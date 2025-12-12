import asyncio
import json

from semantiq.evaluation.llm_evaluator import LLMEvaluator
from semantiq.models.providers.base import BaseModelProvider
from semantiq.schemas import BenchmarkDefinition, ModelAnswer, ModelConfig


class FakeJudgeProvider(BaseModelProvider):
    name = "openai"

    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:
        payload = {"scores": [{"criterion": "clarity", "score": 0.9, "comment": "ok"}]}
        text = json.dumps(payload)
        return ModelAnswer(
            benchmark_id="",
            model_id=f"openai:{config.model_name}",
            model=config.model_name,
            provider="openai",
            answer_text=text,
            raw_response={},
            usage_meta=None,
            finish_reason="stop",
            timestamp=__import__("datetime").datetime.utcnow(),
        )


async def _run_eval():
    prov = FakeJudgeProvider()
    cfg = ModelConfig(provider="openai", model_name="gpt-4o-mini")
    ev = LLMEvaluator(prov, cfg)
    b = BenchmarkDefinition(id="b1", module="SMF", prompt_text="Q", dimensions=["clarity"], meta={})
    a = ModelAnswer(benchmark_id="b1", model_id="openai:gpt-4o-mini", model="gpt-4o-mini", provider="openai", answer_text="Answer", raw_response={}, usage_meta=None, finish_reason="stop", timestamp=__import__("datetime").datetime.utcnow())
    return await ev.evaluate(b, a)


def test_llm_evaluator_basic():
    res = asyncio.run(_run_eval())
    assert res.benchmark_id == "b1"
    assert len(res.scores) == 1
    assert res.scores[0].criterion.value == "clarity"
