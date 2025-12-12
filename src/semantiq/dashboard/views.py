from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.eval_jsonl import read_evaluation_results


def build_router(answers_dir: str, evals_dir: str) -> APIRouter:
    router = APIRouter()
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

    def list_runs() -> list[dict[str, Any]]:
        runs: list[dict[str, Any]] = []
        a_dir = Path(answers_dir)
        if not a_dir.exists():
            return runs
        for p in sorted(a_dir.glob("*.jsonl")):
            items = read_answers_jsonl(str(p))
            model = items[0].model if items else None
            provider = items[0].provider if items else None
            runs.append({"name": p.name, "path": str(p), "count": len(items), "model": model, "provider": provider})
        return runs

    def load_all_evals() -> list:
        e_dir = Path(evals_dir)
        results = []
        if not e_dir.exists():
            return results
        for p in sorted(e_dir.glob("*.jsonl")):
            results.extend(read_evaluation_results(str(p)))
        return results

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        runs = list_runs()
        return templates.TemplateResponse("index.html", {"request": request, "runs": runs})

    @router.get("/runs", response_class=HTMLResponse)
    async def runs_view(request: Request):
        runs = list_runs()
        return templates.TemplateResponse("runs.html", {"request": request, "runs": runs})

    @router.get("/runs/{name}", response_class=HTMLResponse)
    async def run_detail(request: Request, name: str):
        target = Path(answers_dir) / name
        answers = read_answers_jsonl(str(target))
        evals = load_all_evals()
        avg: dict[str, float] = {}
        counts: dict[str, int] = {}
        for e in evals:
            if answers and e.model == (answers[0].model or "") and e.provider == (answers[0].provider or ""):
                for s in e.scores:
                    k = s.criterion.value
                    avg[k] = avg.get(k, 0.0) + s.score
                    counts[k] = counts.get(k, 0) + 1
        for k in list(avg.keys()):
            c = counts.get(k, 1)
            avg[k] = avg[k] / c if c else 0.0
        return templates.TemplateResponse(
            "model_detail.html",
            {
                "request": request,
                "name": name,
                "answers_count": len(answers),
                "model": answers[0].model if answers else None,
                "provider": answers[0].provider if answers else None,
                "averages": avg,
            },
        )

    @router.get("/benchmarks", response_class=HTMLResponse)
    async def benchmarks_view(request: Request):
        a_dir = Path(answers_dir)
        evals = load_all_evals()
        bench_models: dict[str, dict[str, list[float]]] = {}
        for p in sorted(a_dir.glob("*.jsonl")):
            answers = read_answers_jsonl(str(p))
            for ans in answers:
                key = ans.benchmark_id
                mod = ans.model or ""
                if key not in bench_models:
                    bench_models[key] = {}
                bench_models[key].setdefault(mod, [])
        for e in evals:
            for s in e.scores:
                b = e.benchmark_id
                m = e.model
                if b in bench_models:
                    bench_models[b].setdefault(m, []).append(s.score)
        table: list[dict[str, Any]] = []
        for b, models in bench_models.items():
            row = {"benchmark_id": b, "models": []}
            for m, vals in models.items():
                mean = sum(vals) / len(vals) if vals else 0.0
                row["models"].append({"model": m, "score": round(mean, 3)})
            table.append(row)
        return templates.TemplateResponse("benchmark_detail.html", {"request": request, "rows": table})

    return router

