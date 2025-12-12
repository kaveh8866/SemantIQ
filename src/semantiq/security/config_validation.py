from __future__ import annotations

from typing import List

from semantiq.schemas import ModelConfig


def validate_config(config: ModelConfig) -> List[str]:
    warnings: List[str] = []
    if not config.model_name:
        warnings.append("model_name is empty")
    if config.provider in {"openai", "grok"} and not config.api_key:
        warnings.append("api_key missing for provider")
    if config.temperature is not None and not (0.0 <= float(config.temperature) <= 1.0):
        warnings.append("temperature out of range [0.0,1.0]")
    if config.top_p is not None and not (0.0 <= float(config.top_p) <= 1.0):
        warnings.append("top_p out of range [0.0,1.0]")
    if config.max_tokens is not None and int(config.max_tokens) <= 0:
        warnings.append("max_tokens must be > 0")
    return warnings
