"""Download repository implementation using file-based storage."""

import json
from pathlib import Path

import aiofiles
import aiofiles.os
from domain.entities import Download
from domain.value_objects import VideoId


class DownloadRepository:
    """File-based implementation of download repository."""

    def __init__(self, outputs_dir: Path) -> None:
        """Initialize repository with outputs directory."""
        self.outputs_dir = outputs_dir
        self.info_dir = outputs_dir / "info"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.info_dir.mkdir(parents=True, exist_ok=True)

    def _get_info_path(self, video_id: VideoId) -> Path:
        """Get file path for video info."""
        return self.info_dir / f"{video_id}.json"

    async def save(self, download: Download) -> None:
        """Save download information to JSON file asynchronously."""
        path = self._get_info_path(download.video_id)
        data = {
            "id": str(download.video_id),
            "title": download.title,
        }

        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(data, indent=2))

    async def get(self, video_id: VideoId) -> Download | None:
        """Get download by video ID asynchronously."""
        # List files in outputs directory
        files = await aiofiles.os.listdir(str(self.outputs_dir))

        for filename in files:
            if filename.endswith(".mp3") and f"[{video_id}]" in filename:
                file_path = self.outputs_dir / filename
                title = filename.split("[")[0].strip()

                # Get file size asynchronously
                stat = await aiofiles.os.stat(str(file_path))
                file_size = stat.st_size

                return Download(
                    video_id=video_id,
                    title=title,
                    file_path=file_path,
                    file_size=file_size,
                )

        return None

    async def exists(self, video_id: VideoId) -> bool:
        """Check if download exists asynchronously."""
        files = await aiofiles.os.listdir(str(self.outputs_dir))

        for filename in files:
            if filename.endswith(".mp3") and f"[{video_id}]" in filename:
                return True
        return False

    async def list_all(self) -> list[Download]:
        """List all downloads asynchronously."""
        downloads = []

        files = await aiofiles.os.listdir(str(self.outputs_dir))

        for filename in files:
            if not filename.endswith(".mp3"):
                continue

            try:
                # Extract video ID from filename: "Title [video_id].mp3"
                video_id_str = filename.split("[")[-1].split("]")[0]
                title = filename.split("[")[0].strip()

                file_path = self.outputs_dir / filename
                stat = await aiofiles.os.stat(str(file_path))
                file_size = stat.st_size

                video_id = VideoId(value=video_id_str)
                download = Download(
                    video_id=video_id,
                    title=title,
                    file_path=file_path,
                    file_size=file_size,
                )
                downloads.append(download)
            except (IndexError, ValueError):
                # Skip files with invalid naming format
                continue

        return downloads
