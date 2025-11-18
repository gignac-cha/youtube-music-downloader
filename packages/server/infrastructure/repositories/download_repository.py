"""Download repository implementation using file-based storage."""

import json
from pathlib import Path

from domain.entities import Download
from domain.value_objects import VideoId


class DownloadRepository:
    """File-based implementation of download repository."""

    def __init__(self, outputs_dir: Path) -> None:
        """Initialize repository with outputs directory."""
        self.outputs_dir = outputs_dir
        self.info_dir = outputs_dir / "info"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.info_dir.mkdir(parents=True, exist_ok=True)

    def _get_info_path(self, video_id: VideoId) -> Path:
        """Get file path for video info."""
        return self.info_dir / f"{video_id}.json"

    async def save(self, download: Download) -> None:
        """Save download information to JSON file."""
        path = self._get_info_path(download.video_id)
        data = {
            "id": str(download.video_id),
            "title": download.title,
        }

        with path.open("w") as f:
            json.dump(data, f, indent=2)

    async def get(self, video_id: VideoId) -> Download | None:
        """Get download by video ID."""
        # Find the MP3 file
        for file_path in self.outputs_dir.glob("*.mp3"):
            if f"[{video_id}]" in file_path.name:
                title = file_path.name.split("[")[0].strip()
                file_size = file_path.stat().st_size

                return Download(
                    video_id=video_id,
                    title=title,
                    file_path=file_path,
                    file_size=file_size,
                )

        return None

    async def exists(self, video_id: VideoId) -> bool:
        """Check if download exists."""
        for file_path in self.outputs_dir.glob("*.mp3"):
            if f"[{video_id}]" in file_path.name:
                return True
        return False

    async def list_all(self) -> list[Download]:
        """List all downloads."""
        downloads = []

        for file_path in self.outputs_dir.glob("*.mp3"):
            try:
                # Extract video ID from filename: "Title [video_id].mp3"
                filename = file_path.name
                video_id_str = filename.split("[")[-1].split("]")[0]
                title = filename.split("[")[0].strip()
                file_size = file_path.stat().st_size

                video_id = VideoId(value=video_id_str)
                download = Download(
                    video_id=video_id,
                    title=title,
                    file_path=file_path,
                    file_size=file_size,
                )
                downloads.append(download)
            except (IndexError, ValueError):
                # Skip files with invalid naming format
                continue

        return downloads
