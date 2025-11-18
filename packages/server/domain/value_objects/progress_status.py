"""Progress status value object."""

from enum import Enum


class ProgressStatus(str, Enum):
    """Enumeration of possible download progress statuses."""

    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    FINISHED = "finished"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value
