from __future__ import annotations

import asyncio
from semantiq.security.logging import get_logger, sanitize_model_response
from datetime import datetime
from typing import Any

from semantiq.models.providers.base import BaseModelProvider
from semantiq.schemas import ModelAnswer, ModelConfig, UsageMeta


logger = get_logger("semantiq.openai")


class OpenAIProvider(BaseModelProvider):
    name = "openai"

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    def _resolve_client(self, api_key: str | None):
        if self._client:
            return self._client
        from openai import OpenAI

        if api_key:
            return OpenAI(api_key=api_key)
        return OpenAI()

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        client = self._resolve_client(config.api_key)
        attempts = 0
        delay = 0.5
        last_exc: Exception | None = None
        errors = _load_openai_errors()
        while attempts < 3:
            try:
                logger.info("Calling OpenAI", extra={"model": config.model_name, "temperature": config.temperature, "top_p": config.top_p, "max_tokens": config.max_tokens})
                resp = client.chat.completions.create(
                    model=config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.temperature,
                    top_p=config.top_p,
                    max_tokens=config.max_tokens,
                    seed=config.seed,
                )
                choice = resp.choices[0]
                text = getattr(choice.message, "content", "") or ""
                usage = getattr(resp, "usage", None)
                finish_reason = getattr(choice, "finish_reason", None) or "unknown"
                usage_meta = UsageMeta(
                    input_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
                    output_tokens=getattr(usage, "completion_tokens", None) if usage else None,
                    cost=None,
                    latency_ms=None,
                )
                cleaned = sanitize_model_response(_asdict(resp))
                return ModelAnswer(
                    benchmark_id="",
                    model_id=f"openai:{config.model_name}",
                    model=config.model_name,
                    provider="openai",
                    answer_text=text,
                    raw_response=cleaned,
                    usage_meta=usage_meta,
                    finish_reason=finish_reason,
                    timestamp=datetime.utcnow(),
                )
            except errors as exc:  # type: ignore[arg-type]
                last_exc = exc
                if _is_retryable(exc):
                    logger.warning("Retryable error; retrying")
                else:
                    logger.error("Non-retryable error; aborting")
                    break
            attempts += 1
            await asyncio.sleep(delay)
            delay *= 2
        if last_exc:
            raise last_exc
        raise RuntimeError("Unknown error in OpenAIProvider")


def _load_openai_errors():
    try:
        from openai import APIError, APIConnectionError, RateLimitError, BadRequestError

        return (RateLimitError, APIConnectionError, APIError, BadRequestError)
    except Exception:
        return (Exception,)


def _is_retryable(exc: Exception) -> bool:
    name = exc.__class__.__name__.lower()
    return any(k in name for k in ["rate", "connection", "timeout"])


def _asdict(obj: Any) -> dict[str, Any]:
    try:
        return obj.model_dump()  # type: ignore[attr-defined]
    except Exception:
        try:
            return obj.to_dict()  # type: ignore[attr-defined]
        except Exception:
            return {}
