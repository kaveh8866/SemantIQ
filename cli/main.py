import typer
import os
from rich.console import Console
from rich.table import Table
from pipeline import PipelineEngine
from pipeline.runner import AutoPipeline
from pipeline.registry import ResultRegistry
from cli.smf_commands import app as smf_app
from cli.hacs_commands import app as hacs_app
from cli.vision_commands import app as vision_app
from cli.ui_commands import app as ui_app
from cli.research_commands import app as research_app
from cli.ops_commands import app as ops_app

app = typer.Typer(
    name="semantiq",
    help="SemantIQ-M-Benchmarks: An Open-Source LLM Benchmark Framework",
    add_completion=False,
)
pipeline_app = typer.Typer(name="pipeline", help="Manage automated pipeline runs")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(smf_app, name="smf")
app.add_typer(hacs_app, name="hacs")
app.add_typer(vision_app, name="vision")
app.add_typer(ui_app, name="ui")
app.add_typer(research_app, name="research")
app.add_typer(ops_app, name="ops")

console = Console()
# Initialize pipeline with the current working directory as base
pipeline = PipelineEngine(base_dir=os.getcwd())
registry = ResultRegistry(base_dir=os.getcwd())

@app.command()
def init():
    """
    Initialize a new benchmark configuration or project structure.
    """
    console.print("[bold green]Initializing SemantIQ project...[/bold green]")
    # Logic to create local config or scaffolding would go here
    console.print("Project initialized (Placeholder).")

@app.command("list")
def list_benchmarks():
    """
    List all available benchmarks.
    """
    benchmarks = pipeline.list_benchmarks()
    
    table = Table(title="Available Benchmarks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Version", style="yellow")
    
    for b in benchmarks:
        table.add_row(b.id, b.name, b.category.value, b.version)
        
    console.print(table)

@app.command()
def run(
    benchmark: str = typer.Argument(..., help="The ID of the benchmark to run"),
    provider: str = typer.Option("dummy", "--provider", "-p", help="The model provider (openai, openrouter, marber, dummy)"),
    model: str = typer.Option("dummy-model", "--model", "-m", help="The specific model name"),
    temperature: float = typer.Option(None, "--temperature", help="Sampling temperature"),
    max_tokens: int = typer.Option(None, "--max-tokens", help="Maximum tokens to generate"),
    seed: int = typer.Option(None, "--seed", help="Random seed for reproducibility"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """
    Run a specific benchmark against a model.
    """
    console.print(f"Running benchmark '{benchmark}' with provider '{provider}' and model '{model}'")
    
    # Filter None values to only pass provided flags
    kwargs = {k: v for k, v in locals().items() if k in ["temperature", "max_tokens", "seed"] and v is not None}
    
    pipeline.run_benchmark(benchmark, provider, model, **kwargs)

@app.command()
def report(
    run_id: str = typer.Argument(None, help="The specific run ID to report on. Defaults to latest."),
):
    """
    Generate and view reports for benchmark runs.
    """
    console.print(f"[bold yellow]Generating report for run: {run_id or 'latest'}[/bold yellow]")
    # Placeholder for reporting logic

@pipeline_app.command("run")
def pipeline_run(
    config_path: str = typer.Argument(..., help="Path to the pipeline config YAML file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate execution without running models")
):
    """
    Execute a pipeline run based on a configuration file.
    """
    console.print(f"[bold blue]Loading pipeline config from:[/bold blue] {config_path}")
    try:
        runner = AutoPipeline(config_path=config_path, base_dir=os.getcwd())
        runner.run(dry_run=dry_run)
        
        # Update registry after run
        console.print("Updating result registry...")
        registry.update_index()
        
    except Exception as e:
        console.print(f"[bold red]Pipeline execution failed:[/bold red] {e}")

@pipeline_app.command("list-runs")
def pipeline_list_runs():
    """
    List all indexed benchmark runs.
    """
    registry.update_index()
    runs = registry.get_index()
    
    table = Table(title="Benchmark Runs")
    table.add_column("Run ID", style="cyan", no_wrap=True)
    table.add_column("Timestamp", style="dim")
    table.add_column("Benchmark", style="green")
    table.add_column("Provider", style="magenta")
    table.add_column("Model", style="yellow")
    table.add_column("Score", style="bold white")
    
    for run in runs:
        score = f"{run.get('mean_score', 0):.2f}"
        table.add_row(
            run.get("run_id"),
            run.get("timestamp"),
            run.get("benchmark_id"),
            run.get("provider"),
            run.get("model"),
            score
        )
    
    console.print(table)

@pipeline_app.command("status")
def pipeline_status():
    """
    Show overall pipeline status (placeholder for now).
    """
    pipeline_list_runs()

if __name__ == "__main__":
    app()
