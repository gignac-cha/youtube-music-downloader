"""Download service for managing video downloads."""

import asyncio
import json
import logging
from pathlib import Path

import aiofiles
from application.services.retry_service import RetryService
from domain.entities import Download, Progress
from domain.exceptions import DownloadNotFoundError
from domain.value_objects import ProgressStatus, VideoId
from infrastructure.repositories import (
    DownloadRepository,
    FileManager,
    ProgressRepository,
)

logger = logging.getLogger(__name__)


class DownloadService:
    """Service for managing video downloads with retry logic."""

    def __init__(
        self,
        progress_repo: ProgressRepository,
        download_repo: DownloadRepository,
        file_manager: FileManager,
        outputs_dir: Path,
        downloader_module,
        retry_service: RetryService | None = None,
    ) -> None:
        """Initialize download service."""
        self.progress_repo = progress_repo
        self.download_repo = download_repo
        self.file_manager = file_manager
        self.outputs_dir = outputs_dir
        self.downloader = downloader_module
        self.retry_service = retry_service or RetryService(
            max_retries=3, base_delay=2.0, max_delay=30.0
        )

    async def initiate_download(self, url: str) -> dict:
        """Initiate a video download asynchronously.

        Args:
            url: YouTube video URL

        Returns:
            Video information dict

        Raises:
            DownloadAlreadyExistsError: If video is already downloaded
        """
        # Get video info (blocking operation, run in thread pool)
        info = await asyncio.to_thread(self.downloader.info, url)
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

                # Save video info asynchronously
                info_path = self.outputs_dir / "info" / f"{video_id}.json"
                info_path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(info_path, "w") as f:
                    await f.write(json.dumps(info, indent=2))

            return info

        # Not downloaded yet, proceed with download
        # Save video info asynchronously
        info_path = self.outputs_dir / "info" / f"{video_id}.json"
        info_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(info_path, "w") as f:
            await f.write(json.dumps(info, indent=2))

        # Create initial progress
        initial_progress = Progress(
            video_id=video_id,
            status=ProgressStatus.PENDING,
        )
        await self.progress_repo.save(initial_progress)

        # Submit download task as background asyncio task
        asyncio.create_task(self._download_video(str(video_id)))

        return info

    async def _download_video(self, video_id: str) -> None:
        """Background task to download video with retry logic.

        Args:
            video_id: Video ID to download
        """
        try:
            # Retry download operation
            await self.retry_service.retry_async(
                lambda: asyncio.to_thread(self.downloader.download, video_id),
                operation_name=f"Download video {video_id}",
                retryable_exceptions=(Exception,),
            )
            logger.info(f"Successfully downloaded video {video_id}")

        except Exception as e:
            # Mark download as failed
            logger.error(f"Failed to download video {video_id}: {e}")

            try:
                vid = VideoId(value=video_id)
                progress = Progress(
                    video_id=vid,
                    status=ProgressStatus.ERROR,
                    error_message=str(e),
                )
                await self.progress_repo.save(progress)
            except Exception as save_error:
                logger.error(f"Failed to save error status: {save_error}")

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
