"""File manager implementation for handling MP3 files."""

from pathlib import Path

from domain.value_objects import VideoId


class FileManager:
    """File manager for MP3 files."""

    def __init__(self, outputs_dir: Path) -> None:
        """Initialize file manager with outputs directory."""
        self.outputs_dir = outputs_dir
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    async def get_file_path(self, video_id: VideoId) -> Path | None:
        """Get file path for a video ID."""
        for file_path in self.outputs_dir.glob("*.mp3"):
            if f"[{video_id}]" in file_path.name:
                return file_path
        return None

    async def file_exists(self, video_id: VideoId) -> bool:
        """Check if file exists for video ID."""
        file_path = await self.get_file_path(video_id)
        return file_path is not None and file_path.exists()

    async def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        if not file_path.exists():
            return 0
        return file_path.stat().st_size

    async def list_all_files(self) -> list[Path]:
        """List all MP3 files."""
        return list(self.outputs_dir.glob("*.mp3"))
