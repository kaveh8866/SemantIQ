from semantiq.schemas import BenchmarkDefinition, ModelConfig, ModelParameters, ModelAnswer
from datetime import datetime


def test_benchmark_definition():
    b = BenchmarkDefinition(
        id="b1", module="SMF", prompt_text="What is meaning?", dimensions=["clarity"], meta={}
    )
    assert b.id == "b1"


def test_model_config_and_answer():
    params = ModelParameters(temperature=0.1, top_p=0.9, max_tokens=256)
    mc = ModelConfig(provider="openai", model_name="gpt-4o-mini", parameters=params)
    ans = ModelAnswer(
        benchmark_id="b1",
        model_id="openai:gpt-4o-mini",
        answer_text="Hello",
        raw_response=None,
        usage_meta=None,
        timestamp=datetime.utcnow(),
    )
    assert mc.provider == "openai"
    assert ans.model_id.startswith("openai:")