from __future__ import annotations

from typing import Any
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from semantiq.db.models import RunDB, AnswerDB, EvaluationDB
from semantiq.models.providers.openai_provider import OpenAIProvider
from semantiq.schemas import ModelConfig


async def aggregate_scores(session: AsyncSession, study_id: int) -> dict[str, Any]:
    res = await session.exec(select(RunDB).where(RunDB.study_id == study_id))
    runs = list(res)
    run_ids = [r.id for r in runs if r.id is not None]
    res2 = await session.exec(select(AnswerDB).where(AnswerDB.run_id.in_(run_ids)))
    answers = list(res2)
    ans_ids = [a.id for a in answers if a.id is not None]
    res3 = await session.exec(select(EvaluationDB).where(EvaluationDB.answer_id.in_(ans_ids)))
    evals = list(res3)
    totals: dict[str, list[float]] = {}
    for e in evals:
        data = e.scores or {}
        arr = data.get("scores") or []
        for item in arr:
            crit = item.get("criterion")
            val = float(item.get("score", 0.0))
            totals.setdefault(crit, []).append(val)
    averages = {k: (sum(v) / len(v) if v else 0.0) for k, v in totals.items()}
    return {"runs": len(runs), "answers": len(answers), "criteria_avg": averages}


async def generate_study_summary(session: AsyncSession, study_id: int, judge_model_name: str = "gpt-4.1") -> str:
    stats = await aggregate_scores(session, study_id)
    prompt = (
        "You are a Senior Data Scientist. Analyze these benchmark scores and produce a clear Markdown summary.\n\n"
        f"Aggregated stats: {stats}\n\n"
        "Identify strengths, weaknesses, anomalies, and provide recommendations.\n"
    )
    provider = OpenAIProvider()
    mc = ModelConfig(provider="openai", model_name=judge_model_name)
    ans = await provider.generate(prompt, mc)
    return ans.answer_text
