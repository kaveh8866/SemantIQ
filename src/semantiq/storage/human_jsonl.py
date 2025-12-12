from __future__ import annotations

import json
from pathlib import Path

from semantiq.schemas.human_evaluation import HumanRating


def write_human_ratings_jsonl(path: str, ratings: list[HumanRating]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in ratings:
            f.write(json.dumps(r.model_dump(mode="json")) + "\n")


def append_human_rating_jsonl(path: str, rating: HumanRating) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rating.model_dump(mode="json")) + "\n")


def read_human_ratings_jsonl(path: str) -> list[HumanRating]:
    p = Path(path)
    if not p.exists():
        return []
    items: list[HumanRating] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                items.append(HumanRating.model_validate(data))
            except Exception:
                continue
    return items
