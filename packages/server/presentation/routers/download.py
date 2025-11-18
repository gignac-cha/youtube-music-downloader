"""Download router."""

from typing import Annotated

from application.schemas import (
    DownloadedListResponse,
    DownloadRequest,
    DownloadResponse,
    ErrorResponse,
    ProgressResponse,
)
from application.services import DownloadService
from core.config import settings
from core.logging_config import get_logger
from domain.exceptions import DownloadNotFoundError, InvalidVideoIdError
from domain.value_objects import VideoId
from fastapi import APIRouter, Depends, HTTPException, Request, status
from presentation.dependencies import get_download_service
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/api/v1", tags=["download"])
logger = get_logger(__name__)

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/download",
    response_model=DownloadResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid URL"},
        403: {"model": ErrorResponse, "description": "YouTube bot detection"},
        429: {"description": "Too many requests"},
        500: {"model": ErrorResponse, "description": "Download failed"},
    },
)
@limiter.limit(settings.rate_limit_download)
async def initiate_download(
    http_request: Request,
    request: DownloadRequest,
    download_service: Annotated[DownloadService, Depends(get_download_service)],
) -> DownloadResponse:
    """Initiate a video download.

    Args:
        request: Download request with URL

    Returns:
        Download response with video info
    """
    try:
        logger.info(f"Initiating download for URL: {request.url}")
        info = await download_service.initiate_download(request.url)

        logger.info(f"Download initiated for video: {info.get('id')}")
        return DownloadResponse(error=False, data=info)

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Download error: {error_msg}")

        if "bot" in error_msg.lower() or "sign in" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": True,
                    "message": "YouTube bot detection triggered",
                    "details": error_msg,
                },
            )
        elif "403" in error_msg or "forbidden" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": True,
                    "message": "Access denied by YouTube",
                    "details": error_msg,
                },
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": True,
                    "message": "Unexpected error occurred",
                    "details": error_msg,
                },
            )


@router.get(
    "/info/{video_id}",
    response_model=ProgressResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Progress not found"},
        500: {"model": ErrorResponse, "description": "Failed to read progress"},
    },
)
async def get_progress(
    video_id: str,
    download_service: Annotated[DownloadService, Depends(get_download_service)],
) -> ProgressResponse:
    """Get download progress.

    Args:
        video_id: YouTube video ID

    Returns:
        Progress response
    """
    try:
        vid = VideoId(value=video_id)
        progress = await download_service.get_progress(vid)

        return ProgressResponse(error=False, data=progress.to_dict())

    except InvalidVideoIdError as e:
        logger.error(f"Invalid video ID: {video_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": str(e)},
        )
    except DownloadNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "invalid id"},
        )
    except Exception:
        logger.exception("Error getting progress")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": "failed to read progress"},
        )


@router.get(
    "/downloaded",
    response_model=DownloadedListResponse,
)
async def list_downloaded(
    download_service: Annotated[DownloadService, Depends(get_download_service)],
) -> DownloadedListResponse:
    """List all downloaded files.

    Returns:
        List of downloaded files
    """
    try:
        downloads = await download_service.list_downloads()

        data = [download.to_dict() for download in downloads]

        return DownloadedListResponse(error=False, data=data)

    except Exception:
        logger.exception("Error listing downloads")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": "Failed to list downloads"},
        )
