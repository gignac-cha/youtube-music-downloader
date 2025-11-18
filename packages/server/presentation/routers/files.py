"""Files router for serving MP3 files."""

from typing import Annotated

from application.schemas import ErrorResponse
from application.services import FileService
from core.logging_config import get_logger
from domain.exceptions import FileNotFoundError as DomainFileNotFoundError
from domain.exceptions import InvalidVideoIdError
from domain.value_objects import VideoId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from presentation.dependencies import get_file_service

router = APIRouter(tags=["files"])
logger = get_logger(__name__)


@router.get(
    "/download/{video_id}",
    response_class=FileResponse,
    responses={
        404: {"model": ErrorResponse, "description": "File not found"},
    },
)
async def download_file(
    video_id: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileResponse:
    """Download MP3 file.

    Args:
        video_id: YouTube video ID

    Returns:
        File response with MP3 file
    """
    try:
        vid = VideoId(value=video_id)
        file_path = await file_service.get_file_path(vid)

        logger.info(f"Serving file for download: {file_path.name}")
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=file_path.name,
        )

    except (InvalidVideoIdError, DomainFileNotFoundError):
        logger.error(f"File not found: {video_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "file not found"},
        )


@router.get(
    "/play/{video_id}",
    response_class=FileResponse,
    responses={
        404: {"model": ErrorResponse, "description": "File not found"},
    },
)
async def play_file(
    video_id: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileResponse:
    """Stream MP3 file for playback.

    Args:
        video_id: YouTube video ID

    Returns:
        File response with MP3 file
    """
    try:
        vid = VideoId(value=video_id)
        file_path = await file_service.get_file_path(vid)

        logger.info(f"Serving file for playback: {file_path.name}")
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
        )

    except (InvalidVideoIdError, DomainFileNotFoundError):
        logger.error(f"File not found: {video_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "file not found"},
        )
