"""Repository protocol interfaces."""

from pathlib import Path
from typing import Protocol

from domain.entities import Download, Progress, Video
from domain.value_objects import VideoId


class IProgressRepository(Protocol):
    """Interface for progress repository."""

    async def save(self, progress: Progress) -> None:
        """Save progress information."""
        ...

    async def get(self, video_id: VideoId) -> Progress | None:
        """Get progress information by video ID."""
        ...

    async def exists(self, video_id: VideoId) -> bool:
        """Check if progress exists for video ID."""
        ...

    async def delete(self, video_id: VideoId) -> None:
        """Delete progress information."""
        ...


class IDownloadRepository(Protocol):
    """Interface for download repository."""

    async def save(self, download: Download) -> None:
        """Save download information."""
        ...

    async def get(self, video_id: VideoId) -> Download | None:
        """Get download by video ID."""
        ...

    async def exists(self, video_id: VideoId) -> bool:
        """Check if download exists."""
        ...

    async def list_all(self) -> list[Download]:
        """List all downloads."""
        ...


class IFileManager(Protocol):
    """Interface for file management."""

    async def get_file_path(self, video_id: VideoId) -> Path | None:
        """Get file path for a video ID."""
        ...

    async def file_exists(self, video_id: VideoId) -> bool:
        """Check if file exists for video ID."""
        ...

    async def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        ...

    async def list_all_files(self) -> list[Path]:
        """List all MP3 files."""
        ...


class IVideoRepository(Protocol):
    """Interface for video/YouTube operations."""

    async def search(self, query: str) -> list[Video]:
        """Search for videos."""
        ...

    async def get_info(self, url: str) -> dict:
        """Get video information from URL."""
        ...
