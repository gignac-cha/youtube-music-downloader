"""YouTube client for search and video information."""

import json
import urllib.parse

import lxml.etree
import requests
from domain.entities import Video
from domain.exceptions import YouTubeAPIError
from domain.value_objects import VideoId


class YouTubeClient:
    """Client for YouTube search and video information.

    Note: Currently uses HTML scraping. Will be migrated to yt-dlp API in Phase 3.
    """

    def __init__(self, timeout: int = 30) -> None:
        """Initialize YouTube client."""
        self.timeout = timeout

    async def search(self, query: str) -> list[Video]:
        """Search for videos on YouTube.

        Args:
            query: Search query string

        Returns:
            List of Video entities

        Raises:
            YouTubeAPIError: If search fails
        """
        try:
            # Build YouTube search URL
            url = self._build_search_url(query)

            # Make request to YouTube
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Parse HTML response
            videos = self._parse_search_results(response.text)
            return videos

        except requests.RequestException as e:
            raise YouTubeAPIError(f"Failed to search YouTube: {e}") from e
        except Exception as e:
            raise YouTubeAPIError(f"Unexpected error during search: {e}") from e

    def _build_search_url(self, query: str) -> str:
        """Build YouTube search URL."""
        scheme = "https"
        netloc = "www.youtube.com"
        path = "/results"
        params = None
        queries = {
            "search_query": f'{query} "Topic"',
        }
        query_string = urllib.parse.urlencode(queries)
        fragment = None
        return urllib.parse.urlunparse(
            (scheme, netloc, path, params, query_string, fragment)
        )

    def _parse_search_results(self, html: str) -> list[Video]:
        """Parse search results from HTML."""
        videos = []
        root = lxml.etree.HTML(html)
        token = "var ytInitialData = "

        for script in root.xpath(f'//script[starts-with(text(), "{token}")]'):
            data = json.loads(script.text[len(token) : -1])

            contents1 = (
                data.get("contents", {})
                .get("twoColumnSearchResultsRenderer", {})
                .get("primaryContents", {})
                .get("sectionListRenderer", {})
                .get("contents", [])
            )

            for content1 in contents1:
                if "itemSectionRenderer" not in content1:
                    continue

                contents2 = content1["itemSectionRenderer"]["contents"]
                for content2 in contents2:
                    if "videoRenderer" not in content2:
                        continue

                    video_data = content2["videoRenderer"]
                    try:
                        video = self._parse_video_data(video_data)
                        videos.append(video)
                    except (KeyError, ValueError, IndexError):
                        # Skip videos with incomplete data
                        continue

        return videos

    def _parse_video_data(self, video_data: dict) -> Video:
        """Parse individual video data."""
        video_id = VideoId(value=video_data["videoId"])
        title = next(iter(video_data["title"]["runs"]))["text"]
        artist = next(iter(video_data["ownerText"]["runs"]))["text"]

        # Get largest thumbnail
        thumbnail = max(
            video_data["thumbnail"]["thumbnails"],
            key=lambda t: t["width"] ** 2 + t["height"],
        )["url"]

        # Extract view count (optional)
        view_count = None
        if "viewCountText" in video_data:
            view_count = video_data["viewCountText"].get("simpleText", "")

        # Extract duration (optional)
        duration = None
        if "lengthText" in video_data:
            duration = video_data["lengthText"].get("simpleText", "")

        return Video(
            id=video_id,
            title=title,
            artist=artist,
            thumbnail=thumbnail,
            view_count=view_count,
            duration=duration,
        )
