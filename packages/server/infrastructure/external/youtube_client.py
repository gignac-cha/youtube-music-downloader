"""YouTube client for search and video information."""

import asyncio

import yt_dlp
from domain.entities import Video
from domain.exceptions import YouTubeAPIError
from domain.value_objects import VideoId


class YouTubeClient:
    """Client for YouTube search and video information using yt-dlp.

    Uses yt-dlp's native search capabilities for reliable YouTube integration.
    """

    def __init__(self, timeout: int = 30, max_results: int = 20) -> None:
        """Initialize YouTube client.

        Args:
            timeout: Timeout for operations in seconds
            max_results: Maximum number of search results to return
        """
        self.timeout = timeout
        self.max_results = max_results
        self.ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "socket_timeout": timeout,
            "retries": 3,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extractor_args": {
                "youtube": {
                    "player_client": ["ios", "android", "web"],
                    "skip": ["hls", "dash"],
                }
            },
        }

    async def search(self, query: str) -> list[Video]:
        """Search for videos on YouTube using yt-dlp.

        Args:
            query: Search query string

        Returns:
            List of Video entities

        Raises:
            YouTubeAPIError: If search fails
        """
        try:
            # Use yt-dlp's ytsearch: prefix for searching
            # Add "Topic" to find official music channels
            search_url = f'ytsearch{self.max_results}:{query} "Topic"'

            # Run yt-dlp in thread pool to avoid blocking
            results = await asyncio.to_thread(self._search_sync, search_url)

            # Convert results to Video entities
            videos = []
            for entry in results:
                try:
                    video = self._parse_video_entry(entry)
                    videos.append(video)
                except (KeyError, ValueError):
                    # Skip entries with incomplete data
                    continue

            return videos

        except Exception as e:
            raise YouTubeAPIError(f"Failed to search YouTube: {e}") from e

    def _search_sync(self, search_url: str) -> list[dict]:
        """Synchronous search using yt-dlp.

        Args:
            search_url: yt-dlp search URL with ytsearch: prefix

        Returns:
            List of video entry dictionaries
        """
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(search_url, download=False)
            return result.get("entries", [])

    def _parse_video_entry(self, entry: dict) -> Video:
        """Parse video entry from yt-dlp search results.

        Args:
            entry: Video entry dictionary from yt-dlp

        Returns:
            Video entity

        Raises:
            KeyError: If required fields are missing
            ValueError: If video ID is invalid
        """
        # Extract video ID
        video_id = VideoId(value=entry["id"])

        # Extract title
        title = entry.get("title", "Unknown Title")

        # Extract uploader/artist
        artist = entry.get("uploader", entry.get("channel", "Unknown Artist"))

        # Extract thumbnail (prefer best quality)
        thumbnails = entry.get("thumbnails", [])
        if thumbnails:
            # Get highest quality thumbnail
            thumbnail = max(
                thumbnails, key=lambda t: t.get("width", 0) * t.get("height", 0)
            )["url"]
        else:
            # Fallback to default YouTube thumbnail
            thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"

        # Extract view count (optional)
        view_count = None
        if "view_count" in entry:
            views = entry["view_count"]
            if views is not None:
                # Format view count (e.g., "1.4M views")
                if views >= 1_000_000:
                    view_count = f"{views / 1_000_000:.1f}M views"
                elif views >= 1_000:
                    view_count = f"{views / 1_000:.1f}K views"
                else:
                    view_count = f"{views} views"

        # Extract duration (optional)
        duration = None
        if "duration" in entry:
            duration_sec = entry["duration"]
            if duration_sec:
                # Format duration as MM:SS or HH:MM:SS
                hours = duration_sec // 3600
                minutes = (duration_sec % 3600) // 60
                seconds = duration_sec % 60

                if hours > 0:
                    duration = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    duration = f"{minutes}:{seconds:02d}"

        return Video(
            id=video_id,
            title=title,
            artist=artist,
            thumbnail=thumbnail,
            view_count=view_count,
            duration=duration,
        )
