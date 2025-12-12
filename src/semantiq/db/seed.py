from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from semantiq.benchmarks.loader import load_benchmarks
from semantiq.db.engine import get_session, init_db
from semantiq.db.models import BenchmarkDB


def _iter_yaml_files(root: str) -> Iterable[Path]:
    p = Path(root)
    for f in sorted(p.glob("*.yml")):
        yield f
    for f in sorted(p.glob("*.yaml")):
        yield f


async def seed_benchmarks(path: str, force: bool = False) -> int:
    await init_db()
    total = 0
    files = list(_iter_yaml_files(path))
    async with get_session() as session:
        for f in files:
            items = load_benchmarks(str(f))
            for b in items:
                await _upsert_benchmark(session, b.id, b.prompt_text, b.module, b.dimensions, force)
                total += 1
        await session.commit()
    return total


async def _upsert_benchmark(session: AsyncSession, bid: str, prompt: str, module: str, dimensions: list[str], force: bool) -> None:
    existing = await session.exec(select(BenchmarkDB).where(BenchmarkDB.id == bid))
    row = existing.first()
    if row is None:
        session.add(BenchmarkDB(id=bid, prompt=prompt, module=module, dimensions=dimensions))
        return
    if force or row.prompt != prompt or row.module != module or row.dimensions != dimensions:
        row.prompt = prompt
        row.module = module
        row.dimensions = dimensions
        session.add(row)


def seed_benchmarks_sync(path: str, force: bool = False) -> int:
    return asyncio.run(seed_benchmarks(path, force))
