from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from semantiq.schemas import BenchmarkDefinition


def _load_yaml(path: Path) -> list[dict[str, Any]]:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError("YAML support requires PyYAML; use JSON or install PyYAML") from exc
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    return []


def _load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    return []


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def _normalize(item: dict[str, Any]) -> dict[str, Any]:
    if "prompt" in item and "prompt_text" not in item:
        item = {**item, "prompt_text": item["prompt"]}
    return item


def load_benchmarks(path: str) -> list[BenchmarkDefinition]:
    p = Path(path)
    if not p.exists():
        return []
    if p.suffix.lower() in {".yaml", ".yml"}:
        data = _load_yaml(p)
    elif p.suffix.lower() in {".json"}:
        data = _load_json(p)
    elif p.suffix.lower() in {".jsonl"}:
        data = _load_jsonl(p)
    else:
        data = []
    results: list[BenchmarkDefinition] = []
    for item in data:
        try:
            results.append(BenchmarkDefinition.model_validate(_normalize(item)))
        except Exception:
            continue
    return results


def load_benchmarks_many(paths: list[str]) -> list[BenchmarkDefinition]:
    results: list[BenchmarkDefinition] = []
    for p_str in paths:
        results.extend(load_benchmarks(p_str))
    return results