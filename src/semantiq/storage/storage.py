from __future__ import annotations

from typing import Protocol, Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from semantiq.db.models import RunDB, AnswerDB, EvaluationDB, BenchmarkDB


class StorageInterface(Protocol):
    async def create_run(self, session: AsyncSession, model_config: dict) -> RunDB: ...
    async def set_run_status(self, session: AsyncSession, run_id: int, status: str) -> None: ...
    async def list_benchmarks(self, session: AsyncSession) -> list[BenchmarkDB]: ...
    async def get_benchmark_by_id(self, session: AsyncSession, bid: str) -> BenchmarkDB | None: ...
    async def insert_answers(self, session: AsyncSession, run_id: int, rows: Sequence[dict]) -> list[AnswerDB]: ...
    async def insert_evaluations(self, session: AsyncSession, rows: Sequence[dict]) -> list[EvaluationDB]: ...
    async def get_run(self, session: AsyncSession, run_id: int) -> RunDB | None: ...
    async def get_run_results(self, session: AsyncSession, run_id: int) -> list[AnswerDB]: ...


class PostgresStorage:
    async def create_run(self, session: AsyncSession, model_config: dict) -> RunDB:
        run = RunDB(model_config=model_config)
        session.add(run)
        await session.commit()
        await session.refresh(run)
        return run

    async def set_run_status(self, session: AsyncSession, run_id: int, status: str) -> None:
        run = await session.get(RunDB, run_id)
        if not run:
            return
        run.status = status
        await session.commit()

    async def list_benchmarks(self, session: AsyncSession) -> list[BenchmarkDB]:
        res = await session.exec(select(BenchmarkDB))
        return list(res)

    async def get_benchmark_by_id(self, session: AsyncSession, bid: str) -> BenchmarkDB | None:
        return await session.get(BenchmarkDB, bid)

    async def insert_answers(self, session: AsyncSession, run_id: int, rows: Sequence[dict]) -> list[AnswerDB]:
        created: list[AnswerDB] = []
        for r in rows:
            ans = AnswerDB(
                run_id=run_id,
                benchmark_id=r["benchmark_id"],
                answer_text=r["answer_text"],
                usage=r.get("usage", {}),
            )
            session.add(ans)
            created.append(ans)
        await session.commit()
        for ans in created:
            await session.refresh(ans)
        return created

    async def insert_evaluations(self, session: AsyncSession, rows: Sequence[dict]) -> list[EvaluationDB]:
        created: list[EvaluationDB] = []
        for r in rows:
            ev = EvaluationDB(
                answer_id=r["answer_id"],
                scores=r.get("scores", {}),
                source=r.get("source", "ai"),
            )
            session.add(ev)
            created.append(ev)
        await session.commit()
        for ev in created:
            await session.refresh(ev)
        return created

    async def get_run(self, session: AsyncSession, run_id: int) -> RunDB | None:
        return await session.get(RunDB, run_id)

    async def get_run_results(self, session: AsyncSession, run_id: int) -> list[AnswerDB]:
        res = await session.exec(select(AnswerDB).where(AnswerDB.run_id == run_id))
        return list(res)

