"""Domain exceptions."""

from domain.exceptions.domain_exceptions import (
    DomainException,
    DownloadAlreadyExistsError,
    DownloadNotFoundError,
    FileNotFoundError,
    InvalidProgressStatusError,
    InvalidVideoIdError,
    VideoNotFoundError,
    YouTubeAPIError,
)

__all__ = [
    "DomainException",
    "VideoNotFoundError",
    "InvalidVideoIdError",
    "DownloadNotFoundError",
    "DownloadAlreadyExistsError",
    "InvalidProgressStatusError",
    "FileNotFoundError",
    "YouTubeAPIError",
]
