"""File service for file operations."""

from pathlib import Path

from domain.exceptions import FileNotFoundError as DomainFileNotFoundError
from domain.value_objects import VideoId
from infrastructure.repositories import FileManager


class FileService:
    """Service for file operations."""

    def __init__(self, file_manager: FileManager) -> None:
        """Initialize file service."""
        self.file_manager = file_manager

    async def get_file_path(self, video_id: VideoId) -> Path:
        """Get file path for a video.

        Args:
            video_id: Video ID

        Returns:
            Path to the file

        Raises:
            DomainFileNotFoundError: If file not found
        """
        file_path = await self.file_manager.get_file_path(video_id)

        if file_path is None or not file_path.exists():
            raise DomainFileNotFoundError(f"File not found for video {video_id}")

        return file_path
