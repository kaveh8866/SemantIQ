from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON


class BenchmarkDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    prompt: str
    module: str
    dimensions: list[str] = Field(sa_column_kwargs={"type_": JSON})

class StudyDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    config: dict = Field(default={}, sa_column_kwargs={"type_": JSON})
    status: str = Field(default="pending")
    created_by: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    runs: list["RunDB"] = Relationship(back_populates="study")


class RunStatus:
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class RunDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = Field(default="pending")
    model_config: dict = Field(default={}, sa_column_kwargs={"type_": JSON})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    answers: list["AnswerDB"] = Relationship(back_populates="run")
    study_id: int | None = Field(default=None, foreign_key="studydb.id")
    study: StudyDB | None = Relationship(back_populates="runs")


class AnswerDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="rundb.id")
    benchmark_id: str = Field(foreign_key="benchmarkdb.id")
    answer_text: str
    usage: dict = Field(default={}, sa_column_kwargs={"type_": JSON})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    run: Optional[RunDB] = Relationship(back_populates="answers")
    evaluations: list["EvaluationDB"] = Relationship(back_populates="answer")


class EvaluationDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int = Field(foreign_key="answerdb.id")
    scores: dict = Field(default={}, sa_column_kwargs={"type_": JSON})
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    answer: Optional[AnswerDB] = Relationship(back_populates="evaluations")

class ReportDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    study_id: int = Field(foreign_key="studydb.id")
    format: str = Field(default="md")
    content: bytes | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
