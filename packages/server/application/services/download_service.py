"""Download service for managing video downloads."""

import asyncio
import concurrent.futures
import json
from pathlib import Path

from domain.entities import Download, Progress
from domain.exceptions import DownloadNotFoundError
from domain.value_objects import ProgressStatus, VideoId
from infrastructure.repositories import (
    DownloadRepository,
    FileManager,
    ProgressRepository,
)


class DownloadService:
    """Service for managing video downloads."""

    def __init__(
        self,
        progress_repo: ProgressRepository,
        download_repo: DownloadRepository,
        file_manager: FileManager,
        outputs_dir: Path,
        executor: concurrent.futures.ThreadPoolExecutor,
        downloader_module,
    ) -> None:
        """Initialize download service."""
        self.progress_repo = progress_repo
        self.download_repo = download_repo
        self.file_manager = file_manager
        self.outputs_dir = outputs_dir
        self.executor = executor
        self.downloader = downloader_module

    async def initiate_download(self, url: str) -> dict:
        """Initiate a video download.

        Args:
            url: YouTube video URL

        Returns:
            Video information dict

        Raises:
            DownloadAlreadyExistsError: If video is already downloaded
        """
        # Get video info
        info = self.downloader.info(url)
        video_id = VideoId(value=info["id"])

        # Check if already downloaded
        already_downloaded = await self.download_repo.exists(video_id)

        if already_downloaded:
            # Create completion status immediately
            existing_file = await self.file_manager.get_file_path(video_id)
            if existing_file:
                file_size = await self.file_manager.get_file_size(existing_file)

                # Create completion progress
                completion_progress = Progress(
                    video_id=video_id,
                    status=ProgressStatus.FINISHED,
                    downloaded_bytes=file_size,
                    total_bytes=file_size,
                )
                await self.progress_repo.save(completion_progress)

                # Save video info
                info_path = self.outputs_dir / "info" / f"{video_id}.json"
                info_path.parent.mkdir(parents=True, exist_ok=True)
                with info_path.open("w") as f:
                    json.dump(info, f)

            return info

        # Not downloaded yet, proceed with download
        # Save video info
        info_path = self.outputs_dir / "info" / f"{video_id}.json"
        info_path.parent.mkdir(parents=True, exist_ok=True)
        with info_path.open("w") as f:
            json.dump(info, f)

        # Create initial progress
        initial_progress = Progress(
            video_id=video_id,
            status=ProgressStatus.PENDING,
        )
        await self.progress_repo.save(initial_progress)

        # Submit download task to executor
        self.executor.submit(
            lambda vid: asyncio.run(self.downloader.download(vid)),
            str(video_id),
        )

        return info

    async def get_progress(self, video_id: VideoId) -> Progress:
        """Get download progress.

        Args:
            video_id: Video ID

        Returns:
            Progress entity

        Raises:
            DownloadNotFoundError: If progress not found
        """
        progress = await self.progress_repo.get(video_id)

        if progress is None:
            raise DownloadNotFoundError(f"No progress found for video {video_id}")

        return progress

    async def list_downloads(self) -> list[Download]:
        """List all completed downloads.

        Returns:
            List of Download entities
        """
        return await self.download_repo.list_all()
