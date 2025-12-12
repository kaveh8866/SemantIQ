from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Depends, HTTPException, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from semantiq.db.engine import get_session, init_db
from semantiq.db.models import RunDB, StudyDB, ReportDB, AnswerDB, EvaluationDB
from semantiq.storage.storage import PostgresStorage
from semantiq.schemas.research import StudyConfig
from semantiq.orchestrator.manager import create_study
from semantiq.agents.analyst import aggregate_scores, generate_study_summary
from semantiq.reporting.generator import render_markdown_report, render_pdf_from_html


app = FastAPI()
storage = PostgresStorage()
API_KEY = os.getenv("SEMANTIQ_API_KEY", "dev-key")

allowed_origins = os.getenv("SEMANTIQ_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.post("/runs", dependencies=[Depends(require_api_key)])
async def create_run(payload: dict, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    run = await storage.create_run(session, model_config=payload.get("model_config", {}))
    return {"run_id": run.id, "status": run.status}


@app.get("/runs/{run_id}", dependencies=[Depends(require_api_key)])
async def get_run(run_id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    run = await storage.get_run(session, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": run.id, "status": run.status, "created_at": run.created_at}

@app.get("/runs", dependencies=[Depends(require_api_key)])
async def list_runs(session: AsyncSession = Depends(get_session)) -> list[dict[str, Any]]:
    res = await session.exec(select(RunDB))
    items = list(res)
    return [
        {
            "run_id": r.id,
            "status": r.status,
            "created_at": r.created_at,
            "model_name": (r.model_config or {}).get("model_name"),
            "provider": (r.model_config or {}).get("provider"),
        }
        for r in items
        if r.id is not None
    ]


@app.get("/runs/{run_id}/results", dependencies=[Depends(require_api_key)])
async def get_run_results(run_id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    results = await storage.get_run_results(session, run_id)
    return {"count": len(results), "answers": [{"id": a.id, "benchmark_id": a.benchmark_id, "answer_text": a.answer_text} for a in results]}


@app.get("/benchmarks", dependencies=[Depends(require_api_key)])
async def list_benchmarks(session: AsyncSession = Depends(get_session)) -> list[dict[str, Any]]:
    items = await storage.list_benchmarks(session)
    return [{"id": b.id, "module": b.module, "prompt": b.prompt, "dimensions": b.dimensions} for b in items]


@app.post("/studies", dependencies=[Depends(require_api_key)])
async def create_study_api(payload: dict, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    cfg = StudyConfig.model_validate(payload)
    result = await create_study(session, cfg)
    return result


@app.post("/playground/run", dependencies=[Depends(require_api_key)])
async def playground_run(payload: dict, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    providers_models = payload.get("models") or []
    benchmarks_data = payload.get("benchmarks_data")
    benchmarks_path = payload.get("benchmarks_path")
    if not providers_models:
        raise HTTPException(status_code=400, detail="models required")
    storage_local = PostgresStorage()
    runs_created: list[int] = []
    # create runs and enqueue jobs
    from arq import create_pool
    from arq.connections import RedisSettings
    redis = await create_pool(RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://localhost:6379")))
    for mc in providers_models:
        run = await storage_local.create_run(session, model_config=mc)
        await redis.enqueue_job(
            "run_benchmark_job",
            run.id,
            mc,
            mc.get("provider"),
            benchmarks_path,
            None,
            benchmarks_data,
        )
        runs_created.append(run.id)
    return {"runs": runs_created}


@app.get("/studies/{study_id}/report", dependencies=[Depends(require_api_key)])
async def get_study_report(study_id: int, format: str = "md", session: AsyncSession = Depends(get_session)) -> Any:
    stats = await aggregate_scores(session, study_id)
    summary = await generate_study_summary(session, study_id)
    # models list from study config
    study = await session.get(StudyDB, study_id)
    models = (study.config or {}).get("models", []) if study else []
    md = render_markdown_report(f"Study #{study_id}", summary, stats, models)
    if format == "pdf":
        pdf = render_pdf_from_html(f"<html><body><pre>{md}</pre></body></html>")
        if pdf is None:
            raise HTTPException(status_code=500, detail="pdf rendering not available")
        rep = ReportDB(study_id=study_id, format="pdf", content=pdf)
        session.add(rep)
        await session.commit()
        return Response(content=pdf, media_type="application/pdf")
    rep = ReportDB(study_id=study_id, format="md", content=md.encode("utf-8"))
    session.add(rep)
    await session.commit()
    return {"report": md}

@app.post("/schedules", dependencies=[Depends(require_api_key)])
async def create_schedule(payload: dict) -> dict[str, Any]:
    # Stub acceptance; scheduling configured in worker via cron functions
    return {"status": "accepted", "payload": payload}

@app.get("/runs/{run_id}/metrics", dependencies=[Depends(require_api_key)])
async def get_run_metrics(run_id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    res = await session.exec(select(AnswerDB).where(AnswerDB.run_id == run_id))
    answers = list(res)
    ids = [a.id for a in answers if a.id is not None]
    if not ids:
        return {"run_id": run_id, "averages": {}}
    res2 = await session.exec(select(EvaluationDB).where(EvaluationDB.answer_id.in_(ids)))
    evals = list(res2)
    totals: dict[str, list[float]] = {}
    for e in evals:
        data = e.scores or {}
        arr = data.get("scores") or []
        for item in arr:
            k = str(item.get("criterion"))
            v = float(item.get("score", 0.0))
            totals.setdefault(k, []).append(v)
    averages = {k: (sum(v) / len(v) if v else 0.0) for k, v in totals.items()}
    return {"run_id": run_id, "averages": averages}
