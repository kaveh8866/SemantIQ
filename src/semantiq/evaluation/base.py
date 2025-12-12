from __future__ import annotations

from abc import ABC, abstractmethod

from semantiq.schemas import BenchmarkDefinition, ModelAnswer
from semantiq.schemas.evaluation import EvaluationResult


class BaseEvaluator(ABC):
    @abstractmethod
    async def evaluate(self, benchmark: BenchmarkDefinition, answer: ModelAnswer) -> EvaluationResult:
        raise NotImplementedError
