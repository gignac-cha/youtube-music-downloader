"""API endpoint tests."""

import pytest


@pytest.mark.unit
def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


@pytest.mark.unit
def test_search_validation_empty_query(client):
    """Test search endpoint rejects empty query."""
    response = client.post("/api/v1/search", json={"search_query": ""})
    assert response.status_code == 422


@pytest.mark.unit
def test_search_validation_whitespace_query(client):
    """Test search endpoint rejects whitespace-only query."""
    response = client.post("/api/v1/search", json={"search_query": "   "})
    assert response.status_code == 422


@pytest.mark.unit
def test_search_validation_too_long(client):
    """Test search endpoint rejects excessively long query."""
    long_query = "a" * 501
    response = client.post("/api/v1/search", json={"search_query": long_query})
    assert response.status_code == 422


@pytest.mark.unit
def test_search_validation_xss_attempt(client):
    """Test search endpoint blocks XSS attempts."""
    response = client.post(
        "/api/v1/search", json={"search_query": "<script>alert('xss')</script>"}
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_download_validation_empty_url(client):
    """Test download endpoint rejects empty URL."""
    response = client.post("/api/v1/download", json={"url": ""})
    assert response.status_code == 422


@pytest.mark.unit
def test_download_validation_non_youtube_url(client):
    """Test download endpoint rejects non-YouTube URLs."""
    response = client.post("/api/v1/download", json={"url": "https://example.com"})
    assert response.status_code == 422


@pytest.mark.unit
def test_download_validation_malicious_url(client):
    """Test download endpoint blocks malicious URLs."""
    response = client.post(
        "/api/v1/download", json={"url": "javascript:alert('xss')"}
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_download_validation_url_too_long(client):
    """Test download endpoint rejects excessively long URLs."""
    long_url = "https://youtube.com/" + "a" * 2049
    response = client.post("/api/v1/download", json={"url": long_url})
    assert response.status_code == 422


@pytest.mark.unit
def test_get_progress_invalid_video_id(client):
    """Test progress endpoint with invalid video ID."""
    response = client.get("/api/v1/info/invalid-id-!@#")
    assert response.status_code in [400, 404]
