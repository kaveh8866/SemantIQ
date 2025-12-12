from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from semantiq.evaluation.base import BaseEvaluator
from semantiq.models.providers.base import BaseModelProvider
from semantiq.schemas import BenchmarkDefinition, ModelAnswer, ModelConfig
from semantiq.schemas.evaluation import EvaluationCriterion, EvaluationResult, EvaluationScore


def _default_criteria() -> list[str]:
    return ["clarity", "consistency", "depth"]


def _build_prompt(benchmark: BenchmarkDefinition, answer: ModelAnswer, criteria: list[str]) -> str:
    return (
        "You are an expert semantic evaluator for the SemantIQ benchmark.\n\n"
        "You will be given:\n"
        "1) A benchmark question\n"
        "2) A model answer\n"
        "3) A list of evaluation criteria\n\n"
        "For each criterion, you must assign a score between 0.0 and 1.0, where:\n"
        "- 0.0 = completely fails the criterion\n"
        "- 0.5 = partially satisfies the criterion\n"
        "- 1.0 = fully satisfies the criterion\n\n"
        "You must respond ONLY with valid JSON in the following format:\n\n"
        "{\n  \"scores\": [\n"
        "    { \"criterion\": \"clarity\", \"score\": 0.8, \"comment\": \"...\" },\n"
        "    { \"criterion\": \"consistency\", \"score\": 0.7, \"comment\": \"...\" }\n"
        "  ]\n}\n\n"
        f"Benchmark question:\n{benchmark.prompt_text}\n\n"
        f"Model answer:\n{answer.answer_text}\n\n"
        f"Criteria to evaluate:\n{json.dumps(criteria)}\n"
    )


class LLMEvaluator(BaseEvaluator):
    def __init__(self, model_provider: BaseModelProvider, model_config: ModelConfig):
        self.model_provider = model_provider
        self.model_config = model_config

    async def evaluate(self, benchmark: BenchmarkDefinition, answer: ModelAnswer) -> EvaluationResult:
        criteria = benchmark.dimensions or _default_criteria()
        prompt = _build_prompt(benchmark, answer, criteria)
        logger.info("Evaluating answer", extra={"benchmark_id": benchmark.id, "criteria": criteria})
        judge = await self.model_provider.generate(prompt, self.model_config)
        payload = _parse_scores_payload(sanitize_user_generated_text(judge.answer_text))
        scores: list[EvaluationScore] = []
        for item in payload:
            try:
                crit = EvaluationCriterion(item["criterion"])  
            except Exception:
                continue
            val = float(item.get("score", 0.0))
            scores.append(
                EvaluationScore(
                    answer_id=None,
                    benchmark_id=answer.benchmark_id,
                    model=answer.model or self.model_config.model_name,
                    provider=self.model_config.provider,
                    criterion=crit,
                    score=val,
                    source="ai",
                    comment=item.get("comment"),
                    evaluator_model=self.model_config.model_name,
                    timestamp=datetime.utcnow(),
                )
            )
        return EvaluationResult(
            answer_id=None,
            benchmark_id=answer.benchmark_id,
            model=answer.model or self.model_config.model_name,
            provider=self.model_config.provider,
            scores=scores,
        )


def _parse_scores_payload(text: str) -> list[dict[str, Any]]:
    try:
        data = json.loads(text)
        arr = data.get("scores")
        if isinstance(arr, list):
            return arr
    except Exception:
        pass
    return []
from semantiq.security.logging import get_logger, sanitize_user_generated_text
logger = get_logger("semantiq.evaluator")
