"""Schema validation tests."""

import pytest
from application.schemas.requests import DownloadRequest, SearchRequest
from pydantic import ValidationError


@pytest.mark.unit
class TestSearchRequest:
    """Test SearchRequest validation."""

    def test_valid_search_query(self, mock_search_query):
        """Test valid search query."""
        request = SearchRequest(search_query=mock_search_query)
        assert request.search_query == mock_search_query

    def test_empty_search_query(self):
        """Test empty search query fails validation."""
        with pytest.raises(ValidationError):
            SearchRequest(search_query="")

    def test_whitespace_search_query(self):
        """Test whitespace-only search query fails validation."""
        with pytest.raises(ValidationError):
            SearchRequest(search_query="   ")

    def test_search_query_strips_whitespace(self):
        """Test search query strips leading/trailing whitespace."""
        request = SearchRequest(search_query="  test query  ")
        assert request.search_query == "test query"

    def test_search_query_xss_pattern(self):
        """Test search query blocks XSS patterns."""
        with pytest.raises(ValidationError) as exc_info:
            SearchRequest(search_query="<script>alert('xss')</script>")
        assert "malicious" in str(exc_info.value).lower()

    def test_search_query_sql_injection(self):
        """Test search query blocks SQL injection patterns."""
        with pytest.raises(ValidationError) as exc_info:
            SearchRequest(search_query="'; DROP TABLE users; --")
        assert "malicious" in str(exc_info.value).lower()


@pytest.mark.unit
class TestDownloadRequest:
    """Test DownloadRequest validation."""

    def test_valid_youtube_url(self, mock_youtube_url):
        """Test valid YouTube URL."""
        request = DownloadRequest(url=mock_youtube_url)
        assert request.url == mock_youtube_url

    def test_valid_youtu_be_url(self):
        """Test valid youtu.be short URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        request = DownloadRequest(url=url)
        assert request.url == url

    def test_valid_music_youtube_url(self):
        """Test valid music.youtube.com URL."""
        url = "https://music.youtube.com/watch?v=dQw4w9WgXcQ"
        request = DownloadRequest(url=url)
        assert request.url == url

    def test_empty_url(self):
        """Test empty URL fails validation."""
        with pytest.raises(ValidationError):
            DownloadRequest(url="")

    def test_non_youtube_url(self):
        """Test non-YouTube URL fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            DownloadRequest(url="https://example.com")
        assert "youtube" in str(exc_info.value).lower()

    def test_url_without_protocol(self):
        """Test URL without protocol fails validation."""
        with pytest.raises(ValidationError):
            DownloadRequest(url="youtube.com/watch?v=dQw4w9WgXcQ")

    def test_url_with_javascript_protocol(self):
        """Test URL with javascript: protocol fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            DownloadRequest(url="javascript:alert('xss')")
        assert "malicious" in str(exc_info.value).lower()

    def test_url_with_data_protocol(self):
        """Test URL with data: protocol fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            DownloadRequest(url="data:text/html,<script>alert('xss')</script>")
        assert "malicious" in str(exc_info.value).lower()

    def test_url_too_long(self):
        """Test excessively long URL fails validation."""
        long_url = "https://youtube.com/" + "a" * 2049
        with pytest.raises(ValidationError) as exc_info:
            DownloadRequest(url=long_url)
        assert "too long" in str(exc_info.value).lower()
