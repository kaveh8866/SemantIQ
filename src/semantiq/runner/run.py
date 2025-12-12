from __future__ import annotations

from datetime import datetime

from semantiq.config.schemas import AppConfig
from semantiq.schemas import BenchmarkDefinition, ModelAnswer, UsageMeta


def _model_id(provider: str, model_name: str) -> str:
    return f"{provider}:{model_name}"


def run_benchmarks(config: AppConfig, benchmarks: list[BenchmarkDefinition]) -> list[ModelAnswer]:
    answers: list[ModelAnswer] = []
    for model in config.models:
        for b in benchmarks:
            text = "Hello, SemantIQ Phase 0"
            usage = UsageMeta()
            answers.append(
                ModelAnswer(
                    benchmark_id=b.id,
                    model_id=_model_id(model.provider, model.model_name),
                    answer_text=text,
                    raw_response=None,
                    usage_meta=usage,
                    timestamp=datetime.utcnow(),
                )
            )
    return answers