from __future__ import annotations

from fastapi import FastAPI

from .views import build_router


def create_app(answers_path: str, ratings_path: str, benchmarks_path: str | None = None) -> FastAPI:
    app = FastAPI(title="SemantIQ Human Rater")
    app.include_router(build_router(answers_path, ratings_path, benchmarks_path))
    return app

