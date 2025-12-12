from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from semantiq.schemas import ModelConfig, ModelParameters


class StorageConfig(BaseModel):
    format: Literal["jsonl", "sqlite", "parquet"] = "jsonl"
    output_path: str


class AppConfig(BaseModel):
    models: list[ModelConfig]
    parameters: ModelParameters | None = None
    benchmarks: list[str]
    storage: StorageConfig