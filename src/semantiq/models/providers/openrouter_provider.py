from __future__ import annotations

import asyncio
from datetime import datetime
import httpx

from semantiq.models.providers.base import BaseModelProvider
from semantiq.schemas import ModelAnswer, ModelConfig, UsageMeta
from semantiq.security.logging import get_logger, sanitize_model_response


logger = get_logger("semantiq.openrouter")


class OpenRouterProvider(BaseModelProvider):
    name = "openrouter"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client

    def _resolve_client(self) -> httpx.AsyncClient:
        if self._client:
            return self._client
        return httpx.AsyncClient(timeout=30)

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        client = self._resolve_client()
        model = config.model_name or "openrouter/auto"
        base_url = (config.base_url or "https://openrouter.ai/api/v1").rstrip("/")
        url = f"{base_url}/chat/completions"
        headers = {}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        attempts = 0
        delay = 0.5
        last_exc: Exception | None = None
        while attempts < 3:
            try:
                logger.info("Calling OpenRouter", extra={"model": model, "temperature": config.temperature, "top_p": config.top_p, "max_tokens": config.max_tokens})
                resp = await client.post(
                    url,
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": config.temperature,
                        "top_p": config.top_p,
                        "max_tokens": config.max_tokens,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                choice = (data.get("choices") or [{}])[0]
                message = choice.get("message") or {}
                text = message.get("content") or ""
                usage = data.get("usage") or {}
                finish_reason = choice.get("finish_reason") or "unknown"
                usage_meta = UsageMeta(
                    input_tokens=usage.get("prompt_tokens"),
                    output_tokens=usage.get("completion_tokens"),
                    cost=None,
                    latency_ms=None,
                )
                cleaned = sanitize_model_response(data)
                return ModelAnswer(
                    benchmark_id="",
                    model_id=f"openrouter:{model}",
                    model=model,
                    provider="openrouter",
                    answer_text=text,
                    raw_response=cleaned,
                    usage_meta=usage_meta,
                    finish_reason=finish_reason,
                    timestamp=datetime.utcnow(),
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                name = exc.__class__.__name__.lower()
                if any(k in name for k in ["timeout", "connect", "429", "rate"]):
                    logger.warning("Retryable error; retrying")
                else:
                    logger.error("Non-retryable error; aborting")
                    break
            attempts += 1
            await asyncio.sleep(delay)
            delay *= 2
        if last_exc:
            raise last_exc
        raise RuntimeError("Unknown error in OpenRouterProvider")
