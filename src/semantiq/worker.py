from __future__ import annotations

import os
from typing import Any

from arq import create_pool
from arq.connections import RedisSettings

from semantiq.db.engine import get_session
from semantiq.storage.storage import PostgresStorage
from semantiq.benchmarks.loader import load_benchmarks
from semantiq.runner.runner import BenchmarkRunner
from semantiq.models.providers.openai_provider import OpenAIProvider
from semantiq.models.providers.mock_providers import MockGeminiProvider, MockGrokProvider
from semantiq.config.loader import load_model_config_from_yaml


async def run_benchmark_job(ctx, run_id: int, model_config: dict | None = None, provider_key: str | None = None, benchmarks_path: str | None = None, config_path: str | None = None) -> None:
    storage = PostgresStorage()
    async for session in get_session():
        await storage.set_run_status(session, run_id, "running")
        if model_config is not None and "provider" in model_config:
            mc = type("MC", (), {})()
            mc.provider = model_config.get("provider")
            mc.model_name = model_config.get("model_name", "")
            mc.temperature = model_config.get("temperature")
            mc.top_p = model_config.get("top_p")
            mc.max_tokens = model_config.get("max_tokens")
            mc.seed = model_config.get("seed")
            mc.api_key = None
        else:
            mc = load_model_config_from_yaml(config_path or "config/config.yaml", provider_key or "gemini")
        bms = load_benchmarks(benchmarks_path or "examples/benchmarks/example_benchmarks.json")
        pk = provider_key or (model_config.get("provider") if model_config else "gemini")
        if pk == "openai":
            provider = OpenAIProvider()
        elif pk == "grok":
            from semantiq.models.providers.grok_provider import GrokProvider
            provider = GrokProvider()
        else:
            provider = MockGeminiProvider()
        runner = BenchmarkRunner()
        answers = await runner.run(bms, provider, mc)
        rows = []
        for a in answers:
            rows.append({
                "benchmark_id": a.benchmark_id,
                "answer_text": a.answer_text,
                "usage": a.usage_meta.model_dump(mode="json") if a.usage_meta else {},
            })
        await storage.insert_answers(session, run_id, rows)
        await storage.set_run_status(session, run_id, "completed")


class WorkerSettings:
    functions = [run_benchmark_job]
    redis_settings = RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://localhost:6379"))
