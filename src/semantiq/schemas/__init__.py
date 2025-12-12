from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class BenchmarkDefinition(BaseModel):
    id: str
    module: str
    prompt_text: str
    dimensions: list[str] = Field(default_factory=list)
    meta: dict[str, Any] | None = None


class ModelParameters(BaseModel):
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    top_k: int | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None


class UsageMeta(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost: float | None = None
    latency_ms: int | None = None


class ModelConfig(BaseModel):
    provider: Literal["openai", "gemini", "grok", "openrouter"]
    model_name: str
    parameters: ModelParameters | None = None
    api_key_env: str | None = None
    api_key: str | None = None
    seed: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    response_format: dict[str, Any] | None = None
    base_url: str | None = None
    extra: dict[str, Any] | None = None


class ModelAnswer(BaseModel):
    benchmark_id: str
    model_id: str
    model: str | None = None
    provider: str | None = None
    answer_text: str
    raw_response: dict[str, Any] | None = None
    usage_meta: UsageMeta | None = None
    finish_reason: str | None = None
    timestamp: datetime
