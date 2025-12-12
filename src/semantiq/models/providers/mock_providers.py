from __future__ import annotations

import random
from datetime import datetime

from semantiq.schemas import ModelAnswer, ModelConfig, UsageMeta
from semantiq.models.providers.base import BaseModelProvider


class MockOpenAIProvider(BaseModelProvider):
    name = "openai"

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        text = f"[openai:{config.model_name}] " + random.choice([
            "Mock response A",
            "Mock response B",
            "Mock response C",
        ])
        return ModelAnswer(
            benchmark_id="",
            model_id=f"openai:{config.model_name}",
            answer_text=text,
            raw_response={"provider": "openai", "mock": True},
            usage_meta=UsageMeta(input_tokens=10, output_tokens=20),
            timestamp=datetime.utcnow(),
        )


class MockGeminiProvider(BaseModelProvider):
    name = "gemini"

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        text = f"[gemini:{config.model_name}] " + random.choice([
            "Synthetic reply X",
            "Synthetic reply Y",
            "Synthetic reply Z",
        ])
        return ModelAnswer(
            benchmark_id="",
            model_id=f"gemini:{config.model_name}",
            answer_text=text,
            raw_response={"provider": "gemini", "mock": True},
            usage_meta=UsageMeta(input_tokens=12, output_tokens=18),
            timestamp=datetime.utcnow(),
        )


class MockGrokProvider(BaseModelProvider):
    name = "grok"

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        text = f"[grok:{config.model_name}] " + random.choice([
            "Placeholder output 1",
            "Placeholder output 2",
            "Placeholder output 3",
        ])
        return ModelAnswer(
            benchmark_id="",
            model_id=f"grok:{config.model_name}",
            answer_text=text,
            raw_response={"provider": "grok", "mock": True},
            usage_meta=UsageMeta(input_tokens=9, output_tokens=15),
            timestamp=datetime.utcnow(),
        )