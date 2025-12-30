import pytest
from benchmarks.schema import BenchmarkTestCase, ScoreResult
from benchmarks.scoring import ScorerFactory, ExactMatchScorer, HeuristicScorer

def test_exact_match_scorer():
    scorer = ScorerFactory.get_scorer("exact_match")
    case = BenchmarkTestCase(case_id="1", input="in", expected="out")
    
    # Match
    result = scorer.score(case, "out")
    assert result.score == 1.0
    assert result.metrics["exact_match"] is True
    
    # No Match
    result = scorer.score(case, "wrong")
    assert result.score == 0.0
    assert result.metrics["exact_match"] is False

    # Whitespace normalization
    result = scorer.score(case, "  out  ")
    assert result.score == 1.0

def test_heuristic_scorer():
    scorer = ScorerFactory.get_scorer("heuristic")
    case = BenchmarkTestCase(case_id="1", input="in", expected="def foo():")
    
    # Perfect match (contains expected + not empty)
    result = scorer.score(case, "Sure, here is the code:\ndef foo():\n    pass")
    assert result.score == 1.0
    assert result.metrics["not_empty"] is True
    assert result.metrics["contains_expected"] is True

    # Partial match (not empty, but missing expected)
    result = scorer.score(case, "def bar():")
    assert result.score == 0.5
    assert result.metrics["contains_expected"] is False
    
    # Empty output
    result = scorer.score(case, "")
    assert result.score == 0.0
    assert result.metrics["not_empty"] is False
