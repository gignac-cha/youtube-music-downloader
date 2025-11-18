"""Dependency injection for FastAPI."""

import concurrent.futures
import sys

from application.services import DownloadService, FileService, SearchService
from core.config import settings
from infrastructure.external import YouTubeClient
from infrastructure.repositories import (
    DownloadRepository,
    FileManager,
    ProgressRepository,
)

# Add downloader to path
PROJECT_ROOT = settings.project_root
sys.path.append(str(PROJECT_ROOT / "packages"))

import downloader.download

# Global instances
_executor: concurrent.futures.ThreadPoolExecutor | None = None
_youtube_client: YouTubeClient | None = None
_progress_repo: ProgressRepository | None = None
_download_repo: DownloadRepository | None = None
_file_manager: FileManager | None = None
_search_service: SearchService | None = None
_download_service: DownloadService | None = None
_file_service: FileService | None = None


def get_executor() -> concurrent.futures.ThreadPoolExecutor:
    """Get or create ThreadPoolExecutor."""
    global _executor
    if _executor is None:
        _executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=settings.max_workers
        )
    return _executor


def get_youtube_client() -> YouTubeClient:
    """Get or create YouTube client."""
    global _youtube_client
    if _youtube_client is None:
        _youtube_client = YouTubeClient(timeout=settings.youtube_timeout)
    return _youtube_client


def get_progress_repository() -> ProgressRepository:
    """Get or create progress repository."""
    global _progress_repo
    if _progress_repo is None:
        _progress_repo = ProgressRepository(settings.outputs_dir)
    return _progress_repo


def get_download_repository() -> DownloadRepository:
    """Get or create download repository."""
    global _download_repo
    if _download_repo is None:
        _download_repo = DownloadRepository(settings.outputs_dir)
    return _download_repo


def get_file_manager() -> FileManager:
    """Get or create file manager."""
    global _file_manager
    if _file_manager is None:
        _file_manager = FileManager(settings.outputs_dir)
    return _file_manager


def get_search_service() -> SearchService:
    """Get or create search service."""
    global _search_service
    if _search_service is None:
        youtube_client = get_youtube_client()
        _search_service = SearchService(youtube_client)
    return _search_service


def get_download_service() -> DownloadService:
    """Get or create download service."""
    global _download_service
    if _download_service is None:
        progress_repo = get_progress_repository()
        download_repo = get_download_repository()
        file_manager = get_file_manager()
        executor = get_executor()

        # Set FFmpeg location
        downloader.download.YDL_OPTS["ffmpeg_location"] = settings.ffmpeg_location

        _download_service = DownloadService(
            progress_repo=progress_repo,
            download_repo=download_repo,
            file_manager=file_manager,
            outputs_dir=settings.outputs_dir,
            executor=executor,
            downloader_module=downloader.download,
        )
    return _download_service


def get_file_service() -> FileService:
    """Get or create file service."""
    global _file_service
    if _file_service is None:
        file_manager = get_file_manager()
        _file_service = FileService(file_manager)
    return _file_service
