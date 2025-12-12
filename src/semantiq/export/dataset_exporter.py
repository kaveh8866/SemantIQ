from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable
import warnings

from semantiq.benchmarks.loader import load_benchmarks
from semantiq.schemas import BenchmarkDefinition, ModelAnswer
from semantiq.schemas.evaluation import EvaluationResult
from semantiq.schemas.dataset_metadata import DatasetMetadata
from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.eval_jsonl import read_evaluation_results
from semantiq.storage.human_jsonl import read_human_ratings_jsonl
from semantiq import __version__ as SEMANTIQ_VERSION


class DatasetExporter:
    def __init__(
        self,
        benchmarks_paths: list[str],
        answers_paths: list[str],
        evaluations_paths: list[str] | None = None,
        human_ratings_paths: list[str] | None = None,
    ) -> None:
        self.benchmarks_paths = benchmarks_paths
        self.answers_paths = answers_paths
        self.evaluations_paths = evaluations_paths or []
        self.human_ratings_paths = human_ratings_paths or []

    def export(self, output_dir: str, format: str = "jsonl") -> None:
        out = Path(output_dir)
        (out / "config").mkdir(parents=True, exist_ok=True)

        benchmarks: list[BenchmarkDefinition] = []
        for bp in self.benchmarks_paths:
            try:
                benchmarks.extend(load_benchmarks(bp))
            except Exception as exc:
                warnings.warn(f"Failed to load benchmarks from {bp}: {exc}")
        answers = _concat_lists(read_answers_jsonl, self.answers_paths)
        evaluations = _concat_lists(read_evaluation_results, self.evaluations_paths)
        human_ratings = _concat_lists(read_human_ratings_jsonl, self.human_ratings_paths)

        _normalize_answers_inplace(answers)
        models = sorted({a.model or "" for a in answers if a.model})
        providers = sorted({a.provider or "" for a in answers if a.provider})
        criteria = sorted({c for b in benchmarks for c in b.dimensions})

        _write_jsonl(out / "benchmarks.jsonl", (b.model_dump(mode="json") for b in benchmarks))
        _write_jsonl(out / "model_answers.jsonl", (a.model_dump(mode="json") for a in answers))
        ai_evals = [e for e in evaluations if any(s.source == "ai" for s in e.scores)]
        _write_jsonl(out / "ai_evaluations.jsonl", (e.model_dump(mode="json") for e in ai_evals))
        if human_ratings:
            _write_jsonl(out / "human_ratings.jsonl", (r.model_dump(mode="json") for r in human_ratings))

        _basic_validations(benchmarks, answers, evaluations)

        meta = DatasetMetadata(
            name="SemantIQ Open Benchmark Dataset v0.1",
            version="0.1.0",
            description="Open dataset of LLM answers and evaluations across SemantIQ benchmarks (Phase 0)",
            created_at=datetime.utcnow(),
            semantiq_version=SEMANTIQ_VERSION,
            benchmarks_count=len(benchmarks),
            answers_count=len(answers),
            models=models,
            providers=providers,
            criteria=criteria,
            has_ai_evaluations=len(ai_evals) > 0,
            has_human_ratings=len(human_ratings) > 0,
            license="CC BY 4.0",  # dataset license
        )
        (out / "metadata.json").write_text(json.dumps(meta.model_dump(mode="json"), indent=2), encoding="utf-8")

        (out / "config" / "semantiq_version.txt").write_text(SEMANTIQ_VERSION, encoding="utf-8")
        (out / "config" / "models_used.yaml").write_text(_models_yaml(models, providers), encoding="utf-8")

        (out / "README.md").write_text(_dataset_card(), encoding="utf-8")

        if format in {"parquet", "both"}:
            _write_parquet(out, answers, ai_evals, human_ratings)


def _concat_lists(reader, paths: list[str]):
    items = []
    for p in paths:
        try:
            items.extend(reader(p))
        except Exception:
            continue
    return items


def _write_jsonl(path: Path, items: Iterable[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def _normalize_answers_inplace(answers: list[ModelAnswer]) -> None:
    for a in answers:
        if (not a.model or not a.provider) and ":" in a.model_id:
            try:
                provider, model = a.model_id.split(":", 1)
                a.provider = a.provider or provider
                a.model = a.model or model
            except Exception:
                warnings.warn(f"Unable to parse model_id '{a.model_id}'")


def _basic_validations(benchmarks: list[BenchmarkDefinition], answers: list[ModelAnswer], evaluations: list[EvaluationResult]) -> None:
    bench_ids = {b.id for b in benchmarks}
    for a in answers:
        if a.benchmark_id not in bench_ids:
            warnings.warn(f"Answer references unknown benchmark_id '{a.benchmark_id}'")
        if not a.model or not a.provider:
            warnings.warn(f"Answer missing model/provider for benchmark_id '{a.benchmark_id}' (model_id='{a.model_id}')")
    eval_map: dict[tuple[str, str | None], list[EvaluationResult]] = {}
    for e in evaluations:
        key = (e.benchmark_id, e.model)
        eval_map.setdefault(key, []).append(e)
    for a in answers:
        key = (a.benchmark_id, a.model)
        evs = eval_map.get(key, [])
        if not evs or all(len(e.scores) == 0 for e in evs):
            warnings.warn(f"No evaluation scores for benchmark_id='{a.benchmark_id}', model='{a.model}'")


def _write_parquet(out: Path, answers: list[ModelAnswer], ai_evals: list[EvaluationResult], human_ratings: list) -> None:
    try:
        import pandas as pd  # type: ignore
    except Exception as exc:
        warnings.warn(f"Parquet export requires pandas/pyarrow; skipping: {exc}")
        return
    try:
        a_df = pd.DataFrame([a.model_dump(mode="json") for a in answers])
        e_df = pd.DataFrame([e.model_dump(mode="json") for e in ai_evals])
        r_df = pd.DataFrame([r.model_dump(mode="json") for r in human_ratings]) if human_ratings else None
        a_df.to_parquet(out / "model_answers.parquet")
        e_df.to_parquet(out / "ai_evaluations.parquet")
        if r_df is not None:
            r_df.to_parquet(out / "human_ratings.parquet")
    except Exception as exc:
        warnings.warn(f"Failed to write Parquet files: {exc}")


def _models_yaml(models: list[str], providers: list[str]) -> str:
    lines = ["models:"]
    for m in models:
        lines.append(f"  - name: \"{m}\"")
    lines.append("providers:")
    for p in providers:
        lines.append(f"  - \"{p}\"")
    return "\n".join(lines) + "\n"


def _dataset_card() -> str:
    return """# SemantIQ Open Benchmark Dataset v0.1

## Summary
This dataset bundles model answers, AI evaluations, and optional human ratings across SemantIQ benchmarks. It is intended for research, benchmarking, and evaluator calibration in Phase 0.

## Intended Use
Academic and open-source analysis of semantic-cognitive performance of LLMs. Not for diagnostic or psychological use.

## Dataset Structure
- `benchmarks.jsonl`: BenchmarkDefinition entries
- `model_answers.jsonl`: ModelAnswer entries
- `ai_evaluations.jsonl`: EvaluationResult entries (scores source='ai')
- `human_ratings.jsonl`: HumanRating entries (if present)
- `metadata.json`: summary metadata
- `config/models_used.yaml`: models and providers included
- `config/semantiq_version.txt`: exporter SemantIQ version

## Benchmarks Description
Phase 0 includes semantic-cognitive prompts (e.g., SMF, HACS, WIF, CBF). Prompts are high-level and non-sensitive.

## Models Included
Example: GPT-4.1, Gemini 1.5 Pro, Grok-2 (actual set depends on runs).

## Scoring Dimensions
`clarity`, `consistency`, `depth`, `bias_risk`, `reflection`, `stability`.

## How to Load the Dataset
Python:

```python
import json
answers = [json.loads(l) for l in open('model_answers.jsonl')]
evals = [json.loads(l) for l in open('ai_evaluations.jsonl')]
```

Pandas:

```python
import pandas as pd
answers_df = pd.read_json('model_answers.jsonl', lines=True)
evals_df = pd.read_json('ai_evaluations.jsonl', lines=True)
```

SemantIQ SDK:

```python
from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.eval_jsonl import read_evaluation_results
answers = read_answers_jsonl('model_answers.jsonl')
evals = read_evaluation_results('ai_evaluations.jsonl')
```

## License
Code: MIT. Dataset: CC BY 4.0.

## Limitations & Ethical Considerations
Not a psychological test or diagnostic instrument. Focused on semantic/intellectual evaluation in constrained contexts.

## Citation
```
@dataset{semantiq_open_v0_1,
  title = {SemantIQ Open Benchmark Dataset v0.1},
  version = {0.1.0},
  author = {{SemantIQ Contributors}},
  year = {2025}
}
```
"""
