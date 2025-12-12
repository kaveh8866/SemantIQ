from __future__ import annotations

import json
from pathlib import Path

from semantiq.export.dataset_exporter import DatasetExporter


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_exporter_writes_expected_files(tmp_path: Path):
    # Benchmarks
    bench_path = tmp_path / "bench.json"
    write_jsonl(
        bench_path,
        [
            {
                "id": "b1",
                "module": "SMF",
                "prompt_text": "Explain X",
                "dimensions": ["clarity", "consistency"],
            }
        ],
    )

    # Answers (model/provider inferred from model_id)
    answers_path = tmp_path / "answers.jsonl"
    write_jsonl(
        answers_path,
        [
            {
                "benchmark_id": "b1",
                "model_id": "gemini:gemini-pro",
                "answer_text": "Hello",
                "raw_response": {"provider": "gemini", "mock": True},
                "usage_meta": {"input_tokens": 1, "output_tokens": 1},
                "timestamp": "2025-01-01T00:00:00Z",
            }
        ],
    )

    out_dir = tmp_path / "dataset"
    exporter = DatasetExporter(
        benchmarks_paths=[str(bench_path)],
        answers_paths=[str(answers_path)],
        evaluations_paths=[],
        human_ratings_paths=[],
    )
    exporter.export(str(out_dir))

    assert (out_dir / "metadata.json").exists()
    assert (out_dir / "benchmarks.jsonl").exists()
    assert (out_dir / "model_answers.jsonl").exists()

    # Check model_answers line count is 1
    with (out_dir / "model_answers.jsonl").open("r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    assert len(lines) == 1
