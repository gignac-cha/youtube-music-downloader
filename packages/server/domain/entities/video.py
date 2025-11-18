"""Video entity representing a YouTube video."""

from dataclasses import dataclass

from domain.value_objects.video_id import VideoId


@dataclass
class Video:
    """Domain entity representing a YouTube video.

    This entity contains all information about a video from YouTube search results.
    """

    id: VideoId
    title: str
    artist: str
    thumbnail: str
    view_count: str | None = None
    duration: str | None = None

    def __post_init__(self) -> None:
        """Validate video data."""
        if not self.title:
            raise ValueError("Video title cannot be empty")
        if not self.artist:
            raise ValueError("Video artist cannot be empty")
        if not self.thumbnail:
            raise ValueError("Video thumbnail URL cannot be empty")

    @property
    def video_id_str(self) -> str:
        """Return the string representation of the video ID."""
        return str(self.id)

    def to_dict(self) -> dict:
        """Convert the video to a dictionary representation."""
        return {
            "id": self.video_id_str,
            "title": self.title,
            "artist": self.artist,
            "thumbnail": self.thumbnail,
            "view_count": self.view_count,
            "duration": self.duration,
        }
