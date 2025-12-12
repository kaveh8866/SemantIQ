from __future__ import annotations

import os
from itertools import product
from typing import Any

from arq import create_pool
from arq.connections import RedisSettings
from sqlmodel.ext.asyncio.session import AsyncSession

from semantiq.db.models import StudyDB, RunDB
from semantiq.storage.storage import PostgresStorage
from semantiq.schemas.research import StudyConfig


async def create_study(session: AsyncSession, config: StudyConfig) -> dict[str, Any]:
    storage = PostgresStorage()
    study = StudyDB(
        name=config.name,
        description=config.description,
        config=config.model_dump(mode="json"),
        status="pending",
        created_by=config.created_by,
    )
    session.add(study)
    await session.commit()
    await session.refresh(study)

    redis = await create_pool(RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://localhost:6379")))
    runs_created: list[int] = []
    matrix = list(product(config.providers, config.models, config.temperatures, config.max_tokens))
    for _ in range(config.repeats):
        for provider, model_name, temperature, max_tokens in matrix:
            mc = {
                "provider": provider,
                "model_name": model_name,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            run = await storage.create_run(session, model_config=mc)
            run.study_id = study.id
            await session.commit()
            runs_created.append(run.id)
            await redis.enqueue_job(
                "run_benchmark_job",
                run.id,
                mc,
                provider,
                config.benchmarks_path,
            )

    study.status = "running"
    await session.commit()
    return {"study_id": study.id, "runs": runs_created}
