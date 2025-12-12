from __future__ import annotations

from pydantic import BaseModel


class StudyConfig(BaseModel):
    name: str
    description: str | None = None
    created_by: str | None = None
    benchmarks_path: str
    providers: list[str]
    models: list[str]
    temperatures: list[float] = [0.1, 0.5, 0.9]
    max_tokens: list[int] = [128, 256]
    repeats: int = 1
