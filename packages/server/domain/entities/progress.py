"""Progress entity representing download progress."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from domain.value_objects.progress_status import ProgressStatus
from domain.value_objects.video_id import VideoId


@dataclass
class Progress:
    """Domain entity representing download progress.

    Tracks the state and progress of a video download operation.
    """

    video_id: VideoId
    status: ProgressStatus
    downloaded_bytes: int = 0
    total_bytes: int = 1
    speed: float = 0.0
    elapsed: float = 0.0
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate progress data."""
        if self.downloaded_bytes < 0:
            raise ValueError("Downloaded bytes cannot be negative")
        if self.total_bytes <= 0:
            raise ValueError("Total bytes must be positive")
        if self.speed < 0:
            raise ValueError("Speed cannot be negative")
        if self.elapsed < 0:
            raise ValueError("Elapsed time cannot be negative")

    @property
    def progress_percentage(self) -> float:
        """Calculate download progress as a percentage."""
        if self.total_bytes == 0:
            return 0.0
        return (self.downloaded_bytes / self.total_bytes) * 100

    @property
    def is_finished(self) -> bool:
        """Check if the download is finished."""
        return self.status == ProgressStatus.FINISHED

    @property
    def has_error(self) -> bool:
        """Check if the download has an error."""
        return self.status == ProgressStatus.ERROR

    def mark_as_finished(self) -> None:
        """Mark the download as finished."""
        self.status = ProgressStatus.FINISHED
        self.downloaded_bytes = self.total_bytes
        self.updated_at = datetime.now(UTC)

    def mark_as_error(self, error_message: str) -> None:
        """Mark the download as having an error."""
        self.status = ProgressStatus.ERROR
        self.error_message = error_message
        self.updated_at = datetime.now(UTC)

    def update_progress(
        self,
        downloaded_bytes: int,
        total_bytes: int,
        speed: float,
        elapsed: float,
    ) -> None:
        """Update the progress with new values."""
        self.downloaded_bytes = downloaded_bytes
        self.total_bytes = total_bytes
        self.speed = speed
        self.elapsed = elapsed
        self.status = ProgressStatus.DOWNLOADING
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """Convert the progress to a dictionary representation."""
        return {
            "info_dict": {"id": str(self.video_id)},
            "status": self.status.value,
            "downloaded_bytes": self.downloaded_bytes,
            "total_bytes": self.total_bytes,
            "speed": self.speed,
            "elapsed": self.elapsed,
            "error_message": self.error_message,
        }
