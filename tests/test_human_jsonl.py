import tempfile
from pathlib import Path
from datetime import datetime

from semantiq.schemas.human_evaluation import HumanRating
from semantiq.schemas.evaluation import EvaluationCriterion
from semantiq.storage.human_jsonl import append_human_rating_jsonl, read_human_ratings_jsonl


def test_append_and_read_human_ratings():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "ratings.jsonl"
        r = HumanRating(
            rating_id="r1",
            answer_id="a1",
            benchmark_id="b1",
            model="m",
            provider="p",
            rater_id=None,
            criterion=EvaluationCriterion.clarity,
            score=0.8,
            comment="ok",
            timestamp=datetime.utcnow(),
        )
        append_human_rating_jsonl(str(p), r)
        items = read_human_ratings_jsonl(str(p))
        assert len(items) == 1
        assert items[0].criterion.value == "clarity"
