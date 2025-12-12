import asyncio
from types import SimpleNamespace

from semantiq.models.providers.grok_provider import GrokProvider
from semantiq.schemas import ModelConfig


class FakeResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status
        self.content = b""

    def json(self):
        return self._data


class FakeAsyncClient:
    async def post(self, url, headers=None, json=None):
        data = {
            "choices": [
                {
                    "message": {"content": "Grok says hello"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 3, "completion_tokens": 5},
            "model": json.get("model", "grok-2-latest"),
        }
        return FakeResponse(data, status=200)


async def _run_generate():
    provider = GrokProvider(client=FakeAsyncClient())
    cfg = ModelConfig(provider="grok", model_name="grok-2-latest", temperature=0.2, max_tokens=64)
    return await provider.generate("Test", cfg)


def test_grok_provider_generate_returns_model_answer():
    ans = asyncio.run(_run_generate())
    assert ans.provider == "grok"
    assert ans.model == "grok-2-latest"
    assert ans.answer_text.startswith("Grok")
    assert ans.finish_reason == "stop"
