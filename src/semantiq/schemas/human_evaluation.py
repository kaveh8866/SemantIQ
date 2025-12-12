from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel

from semantiq.schemas.evaluation import EvaluationCriterion


class HumanRating(BaseModel):
    rating_id: str
    answer_id: str | None = None
    benchmark_id: str
    model: str
    provider: str
    rater_id: str | None = None
    criterion: EvaluationCriterion
    score: float
    comment: str | None = None
    timestamp: datetime


class HumanEvaluationResult(BaseModel):
    answer_id: str | None = None
    benchmark_id: str
    model: str
    provider: str
    ratings: list[HumanRating]
