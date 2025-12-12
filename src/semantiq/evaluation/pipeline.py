from __future__ import annotations

from semantiq.evaluation.base import BaseEvaluator
from semantiq.schemas import BenchmarkDefinition, ModelAnswer
from semantiq.schemas.evaluation import EvaluationResult


class EvaluationPipeline:
    def __init__(self, evaluator: BaseEvaluator):
        self.evaluator = evaluator

    async def evaluate_answers(
        self,
        benchmarks: dict[str, BenchmarkDefinition],
        answers: list[ModelAnswer],
    ) -> list[EvaluationResult]:
        results: list[EvaluationResult] = []
        for ans in answers:
            b = benchmarks.get(ans.benchmark_id)
            if not b:
                continue
            r = await self.evaluator.evaluate(b, ans)
            results.append(r)
        return results
