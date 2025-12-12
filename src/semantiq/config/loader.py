from __future__ import annotations

import json
import os
import tomllib
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from semantiq.config.schemas import AppConfig
from semantiq.schemas import ModelConfig, ModelParameters


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError("YAML support requires PyYAML; use TOML or install PyYAML") from exc
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_config(path: str | os.PathLike[str]) -> AppConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    if p.suffix.lower() in {".toml"}:
        data = _load_toml(p)
    elif p.suffix.lower() in {".yaml", ".yml"}:
        data = _load_yaml(p)
    elif p.suffix.lower() in {".json"}:
        data = _load_json(p)
    else:
        raise ValueError("Unsupported config format; use TOML, YAML, or JSON")
    try:
        return AppConfig.model_validate(data)
    except ValidationError as ve:
        raise ve


def load_model_config_from_yaml(config_path: str, model_key: str) -> ModelConfig:
    p = Path(config_path)
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError("YAML support requires PyYAML; install with extras 'yaml'") from exc
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    models = data.get("models", {})
    m = models.get(model_key)
    if not m:
        raise KeyError(f"Model key not found: {model_key}")
    api_key_value = m.get("api_key")
    if isinstance(api_key_value, str) and api_key_value.startswith("${ENV.") and api_key_value.endswith("}"):
        env_name = api_key_value[6:-1]
        api_key = os.getenv(env_name)
    else:
        api_key = api_key_value
    params = ModelParameters(
        temperature=m.get("temperature"),
        top_p=m.get("top_p"),
        max_tokens=m.get("max_tokens"),
    )
    return ModelConfig(
        provider=model_key,
        model_name=m.get("model_name", ""),
        parameters=params,
        api_key=api_key,
        seed=m.get("seed"),
        temperature=m.get("temperature"),
        top_p=m.get("top_p"),
        max_tokens=m.get("max_tokens"),
        response_format=m.get("response_format"),
        base_url=m.get("base_url"),
        extra=m.get("extra"),
    )
