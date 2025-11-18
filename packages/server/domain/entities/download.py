"""Download entity representing a completed download."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from domain.value_objects.video_id import VideoId


@dataclass
class Download:
    """Domain entity representing a completed download.

    This entity contains information about a successfully downloaded and converted MP3 file.
    """

    video_id: VideoId
    title: str
    file_path: Path
    file_size: int
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate download data."""
        if not self.title:
            raise ValueError("Download title cannot be empty")
        if self.file_size < 0:
            raise ValueError("File size cannot be negative")

    @property
    def video_id_str(self) -> str:
        """Return the string representation of the video ID."""
        return str(self.video_id)

    @property
    def file_name(self) -> str:
        """Return the file name."""
        return self.file_path.name

    def to_dict(self) -> dict:
        """Convert the download to a dictionary representation."""
        return {
            "info_dict": {
                "id": self.video_id_str,
                "title": self.title,
            },
            "total_bytes": self.file_size,
            "status": "completed",
        }
