import json
import tempfile
from pathlib import Path

from semantiq.storage.jsonl import read_model_answers
from semantiq.storage.eval_jsonl import read_evaluation_results


def test_readers_skip_invalid_lines():
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "a.jsonl"
        e = Path(d) / "e.jsonl"
        a.write_text("{}\n{\"benchmark_id\": \"b1\", \"model_id\": \"m\", \"answer_text\": \"t\", \"timestamp\": \"2024-01-01T00:00:00Z\"}\n", encoding="utf-8")
        e.write_text(json.dumps({"answer_id": None, "benchmark_id": "b1", "model": "m", "provider": "p", "scores": []}) + "\ninvalid\n", encoding="utf-8")
        ans = read_model_answers(str(a))
        evs = read_evaluation_results(str(e))
        assert len(ans) == 1
        assert len(evs) == 1
