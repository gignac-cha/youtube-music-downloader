"""Search service for video search operations."""

from domain.entities import Video
from infrastructure.external import YouTubeClient


class SearchService:
    """Service for searching YouTube videos."""

    def __init__(self, youtube_client: YouTubeClient) -> None:
        """Initialize search service."""
        self.youtube_client = youtube_client

    async def search_videos(self, query: str) -> list[Video]:
        """Search for videos on YouTube.

        Args:
            query: Search query string

        Returns:
            List of Video entities

        Raises:
            YouTubeAPIError: If search fails
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        return await self.youtube_client.search(query)
