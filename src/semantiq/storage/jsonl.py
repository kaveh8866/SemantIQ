from __future__ import annotations

import json
from pathlib import Path

from semantiq.schemas import ModelAnswer


def write_answers(answers: list[ModelAnswer], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for ans in answers:
            f.write(json.dumps(ans.model_dump(mode="json")) + "\n")


def write_jsonl(path: str, answers: list[ModelAnswer]) -> None:
    write_answers(answers, Path(path))


def read_answers_jsonl(path: str) -> list[ModelAnswer]:
    p = Path(path)
    if not p.exists():
        return []
    items: list[ModelAnswer] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                items.append(ModelAnswer.model_validate(data))
            except Exception:
                continue
    return items


def read_model_answers(path: str) -> list[ModelAnswer]:
    return read_answers_jsonl(path)
