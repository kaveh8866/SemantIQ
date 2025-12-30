import pytest
from benchmarks.schema import BenchmarkSpec, BenchmarkCategory, ScoringConfig, TestCase, ScoreResult

def test_benchmark_spec_validation():
    # Valid spec
    spec = BenchmarkSpec(
        id="valid_spec_1",
        name="Valid Spec",
        category=BenchmarkCategory.CODE_WRITER,
        version="1.0.0",
        dataset_path="data.json",
        prompt_template_path="prompts/v1",
        prompt_version="1.0.0",
        scoring=ScoringConfig(scorer_type="exact_match", metrics=["exact_match"])
    )
    assert spec.id == "valid_spec_1"

    # Invalid ID
    with pytest.raises(ValueError):
        BenchmarkSpec(
            id="Invalid ID With Spaces",
            name="Invalid",
            category=BenchmarkCategory.CODE_WRITER,
            version="1.0.0",
            dataset_path="data.json",
            prompt_template_path="prompts/v1",
            prompt_version="1.0.0",
            scoring=ScoringConfig(scorer_type="exact_match", metrics=["exact_match"])
        )

def test_test_case_validation():
    case = TestCase(
        case_id="case_001",
        input="Write a function",
        expected="def func():"
    )
    assert case.case_id == "case_001"
