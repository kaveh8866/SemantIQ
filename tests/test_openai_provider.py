import asyncio
from types import SimpleNamespace

from semantiq.models.providers.openai_provider import OpenAIProvider
from semantiq.schemas import ModelConfig


class FakeChatCompletions:
    def create(self, **kwargs):
        choice = SimpleNamespace(message=SimpleNamespace(content="Hello world"), finish_reason="stop")
        usage = SimpleNamespace(prompt_tokens=5, completion_tokens=7)
        return SimpleNamespace(choices=[choice], usage=usage, model=kwargs.get("model", "mock"))


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeChatCompletions())


async def _run_generate():
    provider = OpenAIProvider(client=FakeClient())
    cfg = ModelConfig(provider="openai", model_name="gpt-4.1", temperature=0.1, max_tokens=64)
    return await provider.generate("Test", cfg)


def test_openai_provider_generate_returns_model_answer():
    ans = asyncio.run(_run_generate())
    assert ans.answer_text == "Hello world"
    assert ans.model_id.startswith("openai:")
    assert ans.usage_meta is not None