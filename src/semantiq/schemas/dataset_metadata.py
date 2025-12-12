from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    name: str
    version: str
    description: str
    created_at: datetime
    semantiq_version: str
    benchmarks_count: int
    answers_count: int
    models: list[str]
    providers: list[str]
    criteria: list[str]
    has_ai_evaluations: bool
    has_human_ratings: bool
    license: str

