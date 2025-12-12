from __future__ import annotations

import asyncio
import json
from semantiq.security.logging import get_logger, sanitize_model_response
from datetime import datetime
from typing import Any

from semantiq.models.providers.base import BaseModelProvider
from semantiq.schemas import ModelAnswer, ModelConfig, UsageMeta


logger = get_logger("semantiq.grok")


class GrokProvider(BaseModelProvider):
    name = "grok"

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    def _base_url(self, config: ModelConfig) -> str:
        return (config.base_url or "https://api.x.ai/v1").rstrip("/")

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        url = f"{self._base_url(config)}/chat/completions"
        headers = {
            "Authorization": f"Bearer {('***' if not config.api_key else '***' + str(config.api_key)[-4:])}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": config.model_name,
            "messages": [{"role": "user", "content": prompt}],
        }
        if config.temperature is not None:
            payload["temperature"] = config.temperature
        if config.top_p is not None:
            payload["top_p"] = config.top_p
        if config.max_tokens is not None:
            payload["max_tokens"] = config.max_tokens
        if config.seed is not None:
            payload["seed"] = config.seed

        attempts = 0
        delay = 1.0
        last_exc: Exception | None = None
        while attempts < 3:
            try:
                if self._client is not None:
                    resp = await _post_async(self._client, url, headers, payload)
                else:
                    import httpx

                    async with httpx.AsyncClient(timeout=30.0) as client:
                        resp = await client.post(url, headers=headers, json=payload)
                status = getattr(resp, "status_code", 0)
                data = await _read_json(resp)
                if status >= 400:
                    if status in (429, 500, 502, 503, 504):
                        raise RuntimeError(f"retryable status {status}")
                    raise RuntimeError(f"non-retryable status {status}")
                choice = (data.get("choices") or [{}])[0]
                msg = choice.get("message") or {}
                text = msg.get("content") or ""
                usage = data.get("usage") or {}
                finish_reason = choice.get("finish_reason") or "unknown"
                usage_meta = UsageMeta(
                    input_tokens=usage.get("prompt_tokens"),
                    output_tokens=usage.get("completion_tokens"),
                )
                cleaned = sanitize_model_response(data)
                return ModelAnswer(
                    benchmark_id="",
                    model_id=f"grok:{config.model_name}",
                    model=config.model_name,
                    provider="grok",
                    answer_text=text,
                    raw_response=cleaned,
                    usage_meta=usage_meta,
                    finish_reason=finish_reason,
                    timestamp=datetime.utcnow(),
                )
            except Exception as exc:
                last_exc = exc
                if _is_retryable_exc(exc):
                    logger.warning("Retrying Grok call")
                    await asyncio.sleep(delay)
                    delay *= 2
                    attempts += 1
                    continue
                logger.error("Grok call failed")
                break
        if last_exc:
            raise last_exc
        raise RuntimeError("Unknown error in GrokProvider")


def _is_retryable_exc(exc: Exception) -> bool:
    s = str(exc).lower()
    return any(k in s for k in ["timeout", "retryable", "rate", "connection", "503", "504"]) 


async def _post_async(client: Any, url: str, headers: dict[str, str], payload: dict[str, Any]):
    return await client.post(url, headers=headers, json=payload)


async def _read_json(resp: Any) -> dict[str, Any]:
    if hasattr(resp, "json"):
        try:
            if asyncio.iscoroutinefunction(resp.json):
                return await resp.json()  # type: ignore
            return resp.json()  # type: ignore
        except Exception:
            pass
    body = None
    try:
        body = await resp.aread()  # type: ignore
    except Exception:
        try:
            body = resp.content  # type: ignore
        except Exception:
            body = b"{}"
    try:
        return json.loads(body)
    except Exception:
        return {}
