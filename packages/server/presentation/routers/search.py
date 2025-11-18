"""Search router."""

from typing import Annotated

from application.schemas import ErrorResponse, SearchRequest, SearchResponse
from application.services import SearchService
from core.logging_config import get_logger
from domain.exceptions import YouTubeAPIError
from fastapi import APIRouter, Depends, HTTPException, status
from presentation.dependencies import get_search_service

router = APIRouter(prefix="/api/v1", tags=["search"])
logger = get_logger(__name__)


@router.post(
    "/search",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid search query"},
        500: {"model": ErrorResponse, "description": "Search failed"},
    },
)
async def search_videos(
    request: SearchRequest,
    search_service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    """Search for YouTube videos.

    Args:
        request: Search request with query

    Returns:
        Search response with list of videos
    """
    try:
        logger.info(f"Searching for videos: {request.search_query}")
        videos = await search_service.search_videos(request.search_query)

        # Convert videos to response format
        video_responses = [
            {
                "id": str(video.id),
                "title": video.title,
                "artist": video.artist,
                "thumbnail": video.thumbnail,
                "view_count": video.view_count,
                "duration": video.duration,
            }
            for video in videos
        ]

        logger.info(f"Found {len(videos)} videos")
        return SearchResponse(error=False, data=video_responses)

    except YouTubeAPIError as e:
        logger.error(f"YouTube API error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": "YouTube search failed",
                "details": str(e),
            },
        )
    except ValueError as e:
        logger.error(f"Invalid search query: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": str(e)},
        )
    except Exception as e:
        logger.exception("Unexpected error during search")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": "Unexpected error", "details": str(e)},
        )
