"""Domain-specific exceptions for the YouTube Music Downloader."""


class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class VideoNotFoundError(DomainException):
    """Raised when a video cannot be found."""

    pass


class InvalidVideoIdError(DomainException):
    """Raised when a video ID is invalid."""

    pass


class DownloadNotFoundError(DomainException):
    """Raised when a download record cannot be found."""

    pass


class DownloadAlreadyExistsError(DomainException):
    """Raised when attempting to download a video that's already downloaded."""

    pass


class InvalidProgressStatusError(DomainException):
    """Raised when a progress status is invalid."""

    pass


class FileNotFoundError(DomainException):
    """Raised when a file cannot be found."""

    pass


class YouTubeAPIError(DomainException):
    """Raised when YouTube API/scraping fails."""

    pass
