import pytest
from unittest.mock import MagicMock, patch
import httpx
from core.settings import settings
from adapters.openai_adapter import OpenAIAdapter
from adapters.openrouter_adapter import OpenRouterAdapter
from adapters.marber_adapter import MarberAdapter
from adapters.base import ModelResponse

# Mock settings to avoid needing real env vars
@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setattr(settings, "MARBER_API_KEY", "test-marber-key")
    monkeypatch.setattr(settings, "MARBER_API_URL", "https://api.marber.ai/v1")

def test_openai_adapter_generate():
    adapter = OpenAIAdapter(model_name="gpt-4")
    
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4-0613",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello world"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }

    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
        
        response = adapter.generate("Hi")
        
        assert isinstance(response, ModelResponse)
        assert response.content == "Hello world"
        assert response.model_name == "gpt-4"
        assert response.metadata["usage"]["total_tokens"] == 21
        assert response.metadata["provider"] == "openai"
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["model"] == "gpt-4"
        assert kwargs["json"]["messages"][0]["content"] == "Hi"

def test_openrouter_adapter_generate():
    adapter = OpenRouterAdapter(model_name="openai/gpt-4o")
    
    mock_response = {
        "id": "gen-123",
        "choices": [{
            "message": {
                "content": "OpenRouter response"
            },
            "finish_reason": "stop"
        }],
        "usage": {"total_tokens": 10}
    }

    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
        
        response = adapter.generate("Test")
        
        assert response.content == "OpenRouter response"
        assert response.metadata["provider"] == "openrouter"
        assert "HTTP-Referer" in adapter.client.headers

def test_marber_adapter_generate():
    adapter = MarberAdapter(model_name="llama-3")
    
    mock_response = {
        "id": "marber-123",
        "choices": [{
            "message": {
                "content": "Marber response"
            }
        }],
        "usage": {"total_tokens": 15}
    }

    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
        
        response = adapter.generate("Test")
        
        assert response.content == "Marber response"
        assert response.metadata["provider"] == "marber"

def test_missing_api_key():
    with patch.object(settings, "OPENAI_API_KEY", None):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is not set"):
            OpenAIAdapter(model_name="gpt-4")

def test_retry_logic():
    adapter = OpenAIAdapter(model_name="gpt-4")
    
    with patch("httpx.Client.post") as mock_post:
        # Fail twice then succeed
        mock_post.side_effect = [
            httpx.HTTPStatusError("500 Error", request=MagicMock(), response=MagicMock(status_code=500)),
            httpx.HTTPStatusError("500 Error", request=MagicMock(), response=MagicMock(status_code=500)),
            MagicMock(status_code=200, json=lambda: {
                "choices": [{"message": {"content": "Success"}}],
                "usage": {}
            })
        ]
        
        response = adapter.generate("Retry test")
        assert response.content == "Success"
        assert mock_post.call_count == 3
