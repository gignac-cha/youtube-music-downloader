"""Video ID value object."""

from dataclasses import dataclass

from domain.exceptions.domain_exceptions import InvalidVideoIdError


@dataclass(frozen=True)
class VideoId:
    """Immutable value object representing a YouTube video ID."""

    value: str

    def __post_init__(self) -> None:
        """Validate video ID format."""
        if not self.value:
            raise InvalidVideoIdError("Video ID cannot be empty")
        if not isinstance(self.value, str):
            raise InvalidVideoIdError("Video ID must be a string")
        if len(self.value) != 11:
            raise InvalidVideoIdError("Video ID must be 11 characters long")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"VideoId(value='{self.value}')"
