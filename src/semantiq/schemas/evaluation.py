from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class EvaluationCriterion(str, Enum):
    clarity = "clarity"
    consistency = "consistency"
    depth = "depth"
    bias_risk = "bias_risk"
    reflection = "reflection"
    stability = "stability"


class EvaluationScore(BaseModel):
    answer_id: str | None = None
    benchmark_id: str
    model: str
    provider: str
    criterion: EvaluationCriterion
    score: float
    source: str
    comment: str | None = None
    evaluator_model: str | None = None
    timestamp: datetime


class EvaluationResult(BaseModel):
    answer_id: str | None = None
    benchmark_id: str
    model: str
    provider: str
    scores: list[EvaluationScore]
