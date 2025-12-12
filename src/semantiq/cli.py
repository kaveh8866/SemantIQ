from __future__ import annotations

import asyncio
from pathlib import Path

import typer

from semantiq.benchmarks.loader import load_benchmarks
from semantiq.benchmarks.safety import check_prompt_safety
from semantiq.config.loader import load_model_config_from_yaml
from semantiq.models.providers.mock_providers import (
    MockGeminiProvider,
    MockGrokProvider,
)
from semantiq.models.providers.openai_provider import OpenAIProvider
from semantiq.runner.runner import BenchmarkRunner
from semantiq.storage.jsonl import write_jsonl
from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.eval_jsonl import write_evaluations_jsonl
from semantiq.evaluation.llm_evaluator import LLMEvaluator
from semantiq.evaluation.pipeline import EvaluationPipeline
from semantiq.export.dataset_exporter import DatasetExporter


app = typer.Typer()


@app.command("run")
def run_cmd(benchmarks: Path, provider: str, config: Path, output: Path, unsafe_allow: bool = typer.Option(False, "--unsafe-allow")) -> None:
    logger = get_logger("semantiq.cli")
    bms = load_benchmarks(str(benchmarks))
    if not unsafe_allow:
        for b in bms:
            issues = check_prompt_safety(b.prompt_text)
            for msg in issues:
                typer.echo(f"Warning: benchmark {b.id} {msg}")
    mc = load_model_config_from_yaml(str(config), provider)
    for w in validate_config(mc):
        typer.echo(f"Warning: {w}")
    if provider == "openai":
        provider = OpenAIProvider()
        typer.echo(f"Model: {mc.model_name}")
    elif provider == "gemini":
        provider = MockGeminiProvider()
    elif provider == "grok":
        from semantiq.models.providers.grok_provider import GrokProvider

        provider = GrokProvider()
    else:
        raise typer.BadParameter("Unknown model provider")
    runner = BenchmarkRunner()
    answers = asyncio.run(runner.run(bms, provider, mc, on_progress=lambda msg: typer.echo(msg)))
    write_jsonl(str(output), answers)
    typer.echo(f"Saving answers to {output}")
    typer.echo(f"Wrote {len(answers)} answers to {output}")


if __name__ == "__main__":
    app()


@app.command("evaluate")
def evaluate_cmd(input: Path, output: Path, provider: str = "openai", config: Path = Path("config/config.yaml"), benchmarks: Path | None = None) -> None:
    answers = read_answers_jsonl(str(input))
    if benchmarks is not None:
        b_list = load_benchmarks(str(benchmarks))
    else:
        b_list = []
    b_map = {b.id: b for b in b_list}
    mc = load_model_config_from_yaml(str(config), provider)
    if provider == "openai":
        judge_provider = OpenAIProvider()
    elif provider == "grok":
        from semantiq.models.providers.grok_provider import GrokProvider

        judge_provider = GrokProvider()
    else:
        judge_provider = MockGeminiProvider()
    evaluator = LLMEvaluator(judge_provider, mc)
    pipeline = EvaluationPipeline(evaluator)
    results = asyncio.run(pipeline.evaluate_answers(b_map, answers))
    write_evaluations_jsonl(str(output), results)
    typer.echo(f"Wrote {len(results)} evaluation results to {output}")


@app.command("dashboard")
def dashboard_cmd(answers_dir: Path = Path("outputs"), evals_dir: Path = Path("outputs"), host: str = "127.0.0.1", port: int = 8000) -> None:
    from semantiq.dashboard.app import create_app
    import uvicorn

    app_instance = create_app(str(answers_dir), str(evals_dir))
    uvicorn.run(app_instance, host=host, port=port)


@app.command("human-rater")
def human_rater_cmd(answers: Path, ratings: Path, benchmarks: Path, host: str = "127.0.0.1", port: int = 8001) -> None:
    from semantiq.human_rater.app import create_app
    import uvicorn

    app_instance = create_app(str(answers), str(ratings), str(benchmarks))
    uvicorn.run(app_instance, host=host, port=port)


@app.command("export-dataset")
def export_dataset_cmd(
    benchmarks: Path = typer.Argument(None, help="Benchmarks file (YAML/JSON/JSONL)"),
    out_dir: Path = typer.Argument(None, help="Output dataset directory"),
    benchmarks_opt: list[Path] = typer.Option([], "--benchmarks", help="One or more benchmark files", show_default=False),
    answers: list[Path] = typer.Option([], help="One or more answers JSONL files", show_default=False),
    evaluations: list[Path] = typer.Option([], help="Optional evaluation JSONL files", show_default=False),
    human_ratings: list[Path] = typer.Option([], help="Optional human ratings JSONL files", show_default=False),
    format: str = typer.Option("jsonl", help="Output format: jsonl|parquet|both"),
    out_dir_opt: Path | None = typer.Option(None, "--out-dir", help="Output dataset directory (optional flag)"),
) -> None:
    b_paths: list[str] = [str(benchmarks)] if benchmarks is not None else []
    if benchmarks_opt:
        b_paths.extend(str(p) for p in benchmarks_opt)
    if not b_paths:
        raise typer.BadParameter("Provide benchmarks via positional argument or --benchmarks option")
    exporter = DatasetExporter(
        benchmarks_paths=b_paths,
        answers_paths=[str(p) for p in answers],
        evaluations_paths=[str(p) for p in evaluations],
        human_ratings_paths=[str(p) for p in human_ratings],
    )
    out_dir_final = str(out_dir_opt or out_dir)
    exporter.export(out_dir_final, format=format)
    typer.echo(f"SemantIQ Open Dataset v0.1 exported to {out_dir_final}")
from semantiq.security.config_validation import validate_config
from semantiq.security.logging import get_logger
