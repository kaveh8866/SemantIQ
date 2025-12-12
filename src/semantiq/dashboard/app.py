from __future__ import annotations

from fastapi import FastAPI

from .views import build_router


def create_app(answers_dir: str, evals_dir: str) -> FastAPI:
    app = FastAPI(title="SemantIQ Dashboard")
    app.include_router(build_router(answers_dir, evals_dir))
    return app

