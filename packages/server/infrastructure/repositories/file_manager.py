"""File manager implementation for handling MP3 files."""

from pathlib import Path

import aiofiles.os
from domain.value_objects import VideoId


class FileManager:
    """File manager for MP3 files."""

    def __init__(self, outputs_dir: Path) -> None:
        """Initialize file manager with outputs directory."""
        self.outputs_dir = outputs_dir
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    async def get_file_path(self, video_id: VideoId) -> Path | None:
        """Get file path for a video ID asynchronously."""
        files = await aiofiles.os.listdir(str(self.outputs_dir))

        for filename in files:
            if filename.endswith(".mp3") and f"[{video_id}]" in filename:
                return self.outputs_dir / filename
        return None

    async def file_exists(self, video_id: VideoId) -> bool:
        """Check if file exists for video ID asynchronously."""
        file_path = await self.get_file_path(video_id)
        if file_path is None:
            return False
        return await aiofiles.os.path.exists(str(file_path))

    async def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes asynchronously."""
        if not await aiofiles.os.path.exists(str(file_path)):
            return 0
        stat = await aiofiles.os.stat(str(file_path))
        return stat.st_size

    async def list_all_files(self) -> list[Path]:
        """List all MP3 files asynchronously."""
        files = await aiofiles.os.listdir(str(self.outputs_dir))
        return [
            self.outputs_dir / filename
            for filename in files
            if filename.endswith(".mp3")
        ]
