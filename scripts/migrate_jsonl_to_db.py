from __future__ import annotations

import glob
import json
import os

import anyio
from sqlmodel.ext.asyncio.session import AsyncSession

from semantiq.db.engine import get_session, init_db
from semantiq.storage.storage import PostgresStorage
from semantiq.db.models import BenchmarkDB


async def import_benchmarks(session: AsyncSession, path_pattern: str) -> None:
    for p in glob.glob(path_pattern):
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                b = BenchmarkDB(id=data["id"], prompt=data.get("prompt_text") or data.get("prompt") or "", module=data.get("module") or "", dimensions=data.get("dimensions") or [])
                session.add(b)
    await session.commit()


async def import_answers(session: AsyncSession, path_pattern: str, run_id: int) -> None:
    storage = PostgresStorage()
    rows = []
    for p in glob.glob(path_pattern):
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                rows.append({"benchmark_id": data["benchmark_id"], "answer_text": data["answer_text"], "usage": data.get("usage_meta") or {}})
    if rows:
        await storage.insert_answers(session, run_id, rows)


async def main() -> None:
    async for session in get_session():
        await init_db()
        storage = PostgresStorage()
        run = await storage.create_run(session, model_config={"migrated": True})
        await import_benchmarks(session, os.getenv("BENCHMARKS_JSONL", "datasets/semantiq-open-v0.1/benchmarks.jsonl"))
        await import_answers(session, os.getenv("ANSWERS_JSONL", "datasets/semantiq-open-v0.1/model_answers.jsonl"), run.id)
        await storage.set_run_status(session, run.id, "completed")


if __name__ == "__main__":
    anyio.run(main)
