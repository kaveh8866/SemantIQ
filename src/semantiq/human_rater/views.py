from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from semantiq.benchmarks.loader import load_benchmarks
from semantiq.schemas import ModelAnswer
from semantiq.schemas.evaluation import EvaluationCriterion
from semantiq.schemas.human_evaluation import HumanRating
from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.human_jsonl import append_human_rating_jsonl, read_human_ratings_jsonl


def _answer_id(ans: ModelAnswer) -> str:
    ts = int(ans.timestamp.timestamp())
    return f"{ans.benchmark_id}:{ans.model_id}:{ts}"


def build_router(answers_path: str, ratings_path: str, benchmarks_path: str | None) -> APIRouter:
    router = APIRouter()
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

    answers = read_answers_jsonl(answers_path)
    ratings = read_human_ratings_jsonl(ratings_path)
    rated_ids = {r.answer_id for r in ratings if r.answer_id}
    benchmarks_map: dict[str, Any] = {}
    if benchmarks_path:
        for b in load_benchmarks(benchmarks_path):
            benchmarks_map[b.id] = b

    def _next_unrated() -> ModelAnswer | None:
        for ans in answers:
            aid = _answer_id(ans)
            if aid not in rated_ids:
                return ans
        return None

    @router.get("/rate", response_class=HTMLResponse)
    async def rate(request: Request):
        ans = _next_unrated()
        if not ans:
            return templates.TemplateResponse("thanks.html", {"request": request, "message": "No more answers to rate."})
        b = benchmarks_map.get(ans.benchmark_id)
        criteria = b.dimensions if b and b.dimensions else [c.value for c in EvaluationCriterion]
        return templates.TemplateResponse(
            "rate_answer.html",
            {
                "request": request,
                "answer": ans,
                "benchmark": b,
                "criteria": criteria,
            },
        )

    @router.post("/submit")
    async def submit(
        request: Request,
        benchmark_id: str = Form(...),
        model: str = Form(...),
        provider: str = Form(...),
        answer_id: str = Form(...),
        ratings_payload: str = Form(...),
    ):
        import json

        data = json.loads(ratings_payload)
        items = []
        for item in data:
            crit = EvaluationCriterion(item["criterion"])  
            rating = HumanRating(
                rating_id=str(uuid.uuid4()),
                answer_id=answer_id,
                benchmark_id=benchmark_id,
                model=model,
                provider=provider,
                rater_id=None,
                criterion=crit,
                score=float(item["score"]),
                comment=item.get("comment"),
                timestamp=datetime.utcnow(),
            )
            items.append(rating)
        for r in items:
            append_human_rating_jsonl(ratings_path, r)
        return RedirectResponse(url="/rate", status_code=303)

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("thanks.html", {"request": request, "message": "Welcome to SemantIQ Human Rater"})

    return router

