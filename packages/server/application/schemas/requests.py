"""Pydantic request schemas."""

from pydantic import BaseModel, Field, field_validator


class SearchRequest(BaseModel):
    """Request schema for video search."""

    search_query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query for YouTube videos",
    )

    @field_validator("search_query")
    @classmethod
    def validate_search_query(cls, v: str) -> str:
        """Validate and clean search query."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Search query cannot be empty or whitespace")
        return cleaned

    model_config = {"json_schema_extra": {"example": {"search_query": "Daft Punk"}}}


class DownloadRequest(BaseModel):
    """Request schema for video download."""

    url: str = Field(
        ...,
        min_length=1,
        description="YouTube video URL",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate YouTube URL format."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("URL cannot be empty")
        if not any(
            domain in cleaned
            for domain in [
                "youtube.com",
                "youtu.be",
                "m.youtube.com",
                "music.youtube.com",
            ]
        ):
            raise ValueError("URL must be a valid YouTube URL")
        return cleaned

    model_config = {
        "json_schema_extra": {
            "example": {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        }
    }
