"""Progress repository implementation using file-based storage."""

import json
from pathlib import Path

import aiofiles
import aiofiles.os
from domain.entities import Progress
from domain.value_objects import ProgressStatus, VideoId


class ProgressRepository:
    """File-based implementation of progress repository."""

    def __init__(self, outputs_dir: Path) -> None:
        """Initialize repository with outputs directory."""
        self.outputs_dir = outputs_dir
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    def _get_progress_path(self, video_id: VideoId) -> Path:
        """Get file path for progress data."""
        return self.outputs_dir / f"{video_id}.json"

    async def save(self, progress: Progress) -> None:
        """Save progress information to JSON file asynchronously."""
        path = self._get_progress_path(progress.video_id)
        data = progress.to_dict()

        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(data, indent=2))

    async def get(self, video_id: VideoId) -> Progress | None:
        """Get progress information by video ID asynchronously."""
        path = self._get_progress_path(video_id)

        if not await aiofiles.os.path.exists(str(path)):
            return None

        try:
            async with aiofiles.open(path) as f:
                content = await f.read()
                data = json.loads(content)

            # Handle empty progress files
            if not data:
                return Progress(
                    video_id=video_id,
                    status=ProgressStatus.DOWNLOADING,
                )

            return Progress(
                video_id=video_id,
                status=ProgressStatus(data.get("status", "downloading")),
                downloaded_bytes=data.get("downloaded_bytes", 0),
                total_bytes=data.get("total_bytes", 1),
                speed=data.get("speed", 0.0),
                elapsed=data.get("elapsed", 0.0),
                error_message=data.get("error_message"),
            )
        except (json.JSONDecodeError, KeyError, ValueError):
            # Return default downloading state for corrupted files
            return Progress(
                video_id=video_id,
                status=ProgressStatus.DOWNLOADING,
            )

    async def exists(self, video_id: VideoId) -> bool:
        """Check if progress exists for video ID asynchronously."""
        path = self._get_progress_path(video_id)
        return await aiofiles.os.path.exists(str(path))

    async def delete(self, video_id: VideoId) -> None:
        """Delete progress information asynchronously."""
        path = self._get_progress_path(video_id)
        if await aiofiles.os.path.exists(str(path)):
            await aiofiles.os.remove(str(path))
