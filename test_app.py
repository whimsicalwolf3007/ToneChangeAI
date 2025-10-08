"""Simple tests for ToneShift AI application."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "models_loaded" in data
    assert "uptime" in data


def test_available_emotions():
    """Test available emotions endpoint."""
    response = client.get("/api/emotions")
    assert response.status_code == 200
    data = response.json()
    assert "emotions" in data
    assert isinstance(data["emotions"], list)
    assert len(data["emotions"]) > 0


def test_available_tones():
    """Test available tones endpoint."""
    response = client.get("/api/tones")
    assert response.status_code == 200
    data = response.json()
    assert "tones" in data
    assert isinstance(data["tones"], list)
    assert len(data["tones"]) > 0


def test_root_endpoint():
    """Test root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ToneShift AI" in response.text


@pytest.mark.asyncio
async def test_analyze_emotion():
    """Test emotion analysis endpoint."""
    # Note: This test may fail if models are not loaded
    test_data = {
        "text": "This is amazing! I love it!"
    }
    
    response = client.post("/analyze", json=test_data)
    
    # Should return 200 or 503 (if models not loaded)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "text" in data
        assert "emotion_analysis" in data
        assert "suggestions" in data


@pytest.mark.asyncio
async def test_rewrite_text():
    """Test text rewriting endpoint."""
    # Note: This test may fail if models are not loaded
    test_data = {
        "text": "You need to fix this now!",
        "target_tone": "polite",
        "preserve_meaning": True
    }
    
    response = client.post("/rewrite", json=test_data)
    
    # Should return 200 or 503 (if models not loaded)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "original_text" in data
        assert "rewritten_text" in data
        assert "emotion_analysis" in data
        assert "target_tone" in data
        assert "confidence" in data
        assert "suggestions" in data


def test_invalid_analyze_request():
    """Test emotion analysis with invalid data."""
    # Empty text
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 422  # Validation error
    
    # Missing text
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # Validation error


def test_invalid_rewrite_request():
    """Test text rewriting with invalid data."""
    # Empty text
    response = client.post("/rewrite", json={
        "text": "",
        "target_tone": "polite"
    })
    assert response.status_code == 422  # Validation error
    
    # Missing required fields
    response = client.post("/rewrite", json={"text": "test"})
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__])
