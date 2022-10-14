"""Test API endpoints."""

import fastapi.testclient

from drifting.app import app


def test_api():
    """Test API endpoints."""
    with fastapi.testclient.TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Hello" in response.json()
        assert response.json()["Hello"] == "World"
