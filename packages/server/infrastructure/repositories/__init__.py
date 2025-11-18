"""Infrastructure repositories."""

from infrastructure.repositories.download_repository import DownloadRepository
from infrastructure.repositories.file_manager import FileManager
from infrastructure.repositories.progress_repository import ProgressRepository
from infrastructure.repositories.protocols import (
    IDownloadRepository,
    IFileManager,
    IProgressRepository,
    IVideoRepository,
)

__all__ = [
    # Protocols
    "IProgressRepository",
    "IDownloadRepository",
    "IFileManager",
    "IVideoRepository",
    # Implementations
    "ProgressRepository",
    "DownloadRepository",
    "FileManager",
]
