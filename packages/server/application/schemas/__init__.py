"""Application schemas."""

from application.schemas.requests import DownloadRequest, SearchRequest
from application.schemas.responses import (
    DownloadedListResponse,
    DownloadInfoResponse,
    DownloadResponse,
    ErrorResponse,
    ProgressInfoResponse,
    ProgressResponse,
    SearchResponse,
    VideoResponse,
)

__all__ = [
    # Request schemas
    "SearchRequest",
    "DownloadRequest",
    # Response schemas
    "VideoResponse",
    "ProgressInfoResponse",
    "DownloadInfoResponse",
    "ErrorResponse",
    "SearchResponse",
    "DownloadResponse",
    "ProgressResponse",
    "DownloadedListResponse",
]
