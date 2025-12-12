from __future__ import annotations

from datetime import datetime

from semantiq.schemas import BenchmarkDefinition, ModelAnswer, ModelConfig
from semantiq.models.providers.base import BaseModelProvider


class BenchmarkRunner:
    async def run(
        self,
        benchmarks: list[BenchmarkDefinition],
        model_provider: BaseModelProvider,
        model_config: ModelConfig,
        on_progress: callable | None = None,
    ) -> list[ModelAnswer]:
        results: list[ModelAnswer] = []
        for b in benchmarks:
            if on_progress:
                on_progress(f"Running benchmark {b.id}…")
            ans = await model_provider.generate(b.prompt_text, model_config)
            ans.benchmark_id = b.id
            ans.timestamp = datetime.utcnow()
            results.append(ans)
        return results