"""Pydantic response schemas."""

from pydantic import BaseModel, Field


class VideoResponse(BaseModel):
    """Response schema for a single video."""

    id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    artist: str = Field(..., description="Video artist/channel")
    thumbnail: str = Field(..., description="Thumbnail URL")
    view_count: str | None = Field(None, description="View count")
    duration: str | None = Field(None, description="Video duration")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "dQw4w9WgXcQ",
                "title": "Never Gonna Give You Up",
                "artist": "Rick Astley - Topic",
                "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                "view_count": "1.4B views",
                "duration": "3:32",
            }
        }
    }


class ProgressInfoResponse(BaseModel):
    """Response schema for download progress information."""

    info_dict: dict[str, str] = Field(..., description="Video information")
    status: str = Field(..., description="Download status")
    speed: float = Field(..., description="Download speed in bytes/sec", ge=0)
    downloaded_bytes: int = Field(..., description="Downloaded bytes", ge=0)
    total_bytes: int = Field(..., description="Total bytes", ge=1)
    elapsed: float = Field(..., description="Elapsed time in seconds", ge=0)
    error_message: str | None = Field(None, description="Error message if any")

    model_config = {
        "json_schema_extra": {
            "example": {
                "info_dict": {"id": "dQw4w9WgXcQ"},
                "status": "downloading",
                "speed": 1024000.0,
                "downloaded_bytes": 2048000,
                "total_bytes": 4096000,
                "elapsed": 2.5,
                "error_message": None,
            }
        }
    }


class DownloadInfoResponse(BaseModel):
    """Response schema for completed download information."""

    info_dict: dict[str, str] = Field(..., description="Video information")
    total_bytes: int = Field(..., description="File size in bytes", ge=0)
    status: str = Field(..., description="Download status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "info_dict": {
                    "id": "dQw4w9WgXcQ",
                    "title": "Never Gonna Give You Up",
                },
                "total_bytes": 4096000,
                "status": "completed",
            }
        }
    }


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    error: bool = Field(True, description="Error flag")
    message: str = Field(..., description="Error message")
    details: str | None = Field(None, description="Detailed error information")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": True,
                "message": "Invalid video ID",
                "details": "The provided video ID is not 11 characters long",
            }
        }
    }


class SearchResponse(BaseModel):
    """Response schema for video search."""

    error: bool = Field(False, description="Error flag")
    data: list[VideoResponse] = Field(..., description="List of search results")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": False,
                "data": [
                    {
                        "id": "dQw4w9WgXcQ",
                        "title": "Never Gonna Give You Up",
                        "artist": "Rick Astley - Topic",
                        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                        "view_count": "1.4B views",
                        "duration": "3:32",
                    }
                ],
            }
        }
    }


class DownloadResponse(BaseModel):
    """Response schema for download initiation."""

    error: bool = Field(False, description="Error flag")
    data: dict = Field(..., description="Video information")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": False,
                "data": {
                    "id": "dQw4w9WgXcQ",
                    "title": "Never Gonna Give You Up",
                    "uploader": "Rick Astley - Topic",
                },
            }
        }
    }


class ProgressResponse(BaseModel):
    """Response schema for progress query."""

    error: bool = Field(False, description="Error flag")
    data: ProgressInfoResponse = Field(..., description="Progress information")


class DownloadedListResponse(BaseModel):
    """Response schema for list of downloaded files."""

    error: bool = Field(False, description="Error flag")
    data: list[DownloadInfoResponse] = Field(
        ..., description="List of downloaded files"
    )
