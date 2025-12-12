from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from semantiq.db.engine import get_session, init_db
from semantiq.db.models import RunDB, BenchmarkDB, StudyDB, ReportDB
from semantiq.storage.storage import PostgresStorage
from semantiq.schemas.research import StudyConfig
from semantiq.orchestrator.manager import create_study
from semantiq.agents.analyst import aggregate_scores, generate_study_summary
from semantiq.reporting.generator import render_markdown_report, render_pdf_from_html


app = FastAPI()
storage = PostgresStorage()
API_KEY = os.getenv("SEMANTIQ_API_KEY", "dev-key")


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
