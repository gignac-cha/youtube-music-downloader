"""Custom exception handlers for the application."""

import logging

from domain.exceptions import (
    DownloadNotFoundError,
    FileNotFoundError as DomainFileNotFoundError,
    InvalidVideoIdError,
    YouTubeAPIError,
)
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors with detailed messages."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({"field": field, "message": message})

    logger.warning(f"Validation error on {request.url.path}: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error",
            "details": errors,
        },
    )


async def youtube_api_exception_handler(
    request: Request, exc: YouTubeAPIError
) -> JSONResponse:
    """Handle YouTube API errors."""
    logger.error(f"YouTube API error on {request.url.path}: {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": True,
            "message": "YouTube service temporarily unavailable",
            "details": exc.message,
        },
    )


async def invalid_video_id_exception_handler(
    request: Request, exc: InvalidVideoIdError
) -> JSONResponse:
    """Handle invalid video ID errors."""
    logger.warning(f"Invalid video ID on {request.url.path}: {exc.video_id}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": True,
            "message": "Invalid video ID format",
            "details": str(exc),
        },
    )


async def download_not_found_exception_handler(
    request: Request, exc: DownloadNotFoundError
) -> JSONResponse:
    """Handle download not found errors."""
    logger.info(f"Download not found on {request.url.path}: {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": True,
            "message": "Download not found",
            "details": exc.message,
        },
    )


async def file_not_found_exception_handler(
    request: Request, exc: DomainFileNotFoundError
) -> JSONResponse:
    """Handle file not found errors."""
    logger.info(f"File not found on {request.url.path}: {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": True,
            "message": "File not found",
            "details": exc.message,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors with proper logging and user-friendly messages."""
    logger.exception(f"Unexpected error on {request.url.path}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "details": "Please try again later. If the problem persists, contact support.",
        },
    )
