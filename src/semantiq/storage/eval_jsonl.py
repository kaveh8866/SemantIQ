from __future__ import annotations

import json
from pathlib import Path

from semantiq.schemas.evaluation import EvaluationResult


def write_evaluations_jsonl(path: str, evaluations: list[EvaluationResult]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for e in evaluations:
            f.write(json.dumps(e.model_dump(mode="json")) + "\n")


def read_evaluation_results(path: str) -> list[EvaluationResult]:
    p = Path(path)
    if not p.exists():
        return []
    items: list[EvaluationResult] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                items.append(EvaluationResult.model_validate(data))
            except Exception:
                continue
    return items
