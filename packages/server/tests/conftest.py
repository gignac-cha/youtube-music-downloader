"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client for the application."""
    from main import app

    return TestClient(app)


@pytest.fixture
def mock_video_id():
    """Return a mock video ID for testing."""
    return "dQw4w9WgXcQ"


@pytest.fixture
def mock_youtube_url():
    """Return a mock YouTube URL for testing."""
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture
def mock_search_query():
    """Return a mock search query for testing."""
    return "Daft Punk"
