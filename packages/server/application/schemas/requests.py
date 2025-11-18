"""Pydantic request schemas."""

import re

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

        # Check for suspicious patterns that could indicate injection attempts
        suspicious_patterns = [
            r"<script",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"eval\(",
            r"DROP\s+TABLE",
            r"INSERT\s+INTO",
            r"DELETE\s+FROM",
            r"UPDATE\s+.*\s+SET",
            r"--\s*$",
            r"/\*.*\*/",
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                raise ValueError(
                    "Search query contains potentially malicious content"
                )

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

        # Check length to prevent extremely long URLs
        if len(cleaned) > 2048:
            raise ValueError("URL is too long")

        # Must start with http:// or https://
        if not re.match(r"^https?://", cleaned, re.IGNORECASE):
            raise ValueError("URL must start with http:// or https://")

        # Check for valid YouTube domains
        youtube_domains = [
            "youtube.com",
            "youtu.be",
            "m.youtube.com",
            "music.youtube.com",
        ]
        if not any(domain in cleaned.lower() for domain in youtube_domains):
            raise ValueError("URL must be a valid YouTube URL")

        # Check for suspicious patterns
        suspicious_patterns = [
            r"<script",
            r"javascript:",
            r"data:",
            r"vbscript:",
            r"file://",
            r"\\x",  # Hex encoding attempts
            r"%00",  # Null byte
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                raise ValueError("URL contains potentially malicious content")

        return cleaned

    model_config = {
        "json_schema_extra": {
            "example": {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        }
    }
