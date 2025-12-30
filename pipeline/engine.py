import json
import os
import time
import hashlib
from typing import List, Optional
from datetime import datetime
from rich.console import Console
from jinja2 import Template

from benchmarks.schema import (
    BenchmarkSpec, 
    BenchmarkTestCase, 
    BenchmarkRunResult, 
    CaseResult, 
    BenchmarkCategory, 
    ScoringConfig
)
from benchmarks.scoring import ScorerFactory
from adapters.base import BaseModelAdapter
from adapters import DummyAdapter, OpenAIAdapter, OpenRouterAdapter, MarberAdapter

console = Console()

class PipelineEngine:
    """
    Core execution engine for SemantIQ-M-Benchmarks.
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.benchmarks_dir = os.path.join(base_dir, "benchmarks")
        self.results_dir = os.path.join(base_dir, "runs")
        self.datasets_dir = os.path.join(base_dir, "datasets")
        self.prompts_dir = os.path.join(base_dir, "prompts")

    def _get_adapter(self, provider_name: str, model_name: str) -> BaseModelAdapter:
        if provider_name == "dummy":
            return DummyAdapter(model_name=model_name)
        elif provider_name == "openai":
            return OpenAIAdapter(model_name=model_name)
        elif provider_name == "openrouter":
            return OpenRouterAdapter(model_name=model_name)
        elif provider_name == "marber":
            return MarberAdapter(model_name=model_name)
        
        raise ValueError(f"Unknown provider: {provider_name}")

    def list_benchmarks(self) -> List[BenchmarkSpec]:
        """
        Returns a list of available benchmarks.
        For MVP, we construct a hardcoded list or scan for spec files.
        Here we define the 'code_writer_v1' spec in code for simplicity, 
        but ideally this would be loaded from a YAML/JSON file.
        """
        # MVP: Define the Code Writer V1 Spec programmatically
        spec = BenchmarkSpec(
            id="code_writer_v1",
            name="Code Writer V1",
            category=BenchmarkCategory.CODE_WRITER,
            version="1.0.0",
            dataset_path="code_writer_v1.json",
            prompt_template_path="code_writer/v1",
            prompt_version="1.0.0",
            scoring=ScoringConfig(
                scorer_type="heuristic",
                metrics=["not_empty", "contains_expected"]
            )
        )
        return [spec]

    def _load_dataset(self, dataset_path: str) -> List[BenchmarkTestCase]:
        full_path = os.path.join(self.datasets_dir, dataset_path)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [BenchmarkTestCase(**item) for item in data]

    def _load_prompt_template(self, template_path: str, template_name: str) -> str:
        full_path = os.path.join(self.prompts_dir, template_path, template_name)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def run_benchmark(self, benchmark_id: str, model_provider: str, model_name: str, **kwargs) -> Optional[BenchmarkRunResult]:
        """
        Executes a specific benchmark against a model provider.
        """
        # 1. Load Spec
        specs = self.list_benchmarks()
        spec = next((s for s in specs if s.id == benchmark_id), None)
        if not spec:
            console.print(f"[bold red]Benchmark {benchmark_id} not found.[/bold red]")
            return None

        console.log(f"[bold green]Starting benchmark:[/bold green] {spec.name} ({spec.id})")
        console.log(f"[bold blue]Provider:[/bold blue] {model_provider}")
        console.log(f"[bold blue]Model:[/bold blue] {model_name}")

        # 2. Initialize Adapter
        try:
            adapter = self._get_adapter(model_provider, model_name)
        except ValueError as e:
            console.print(f"[bold red]Error initializing adapter:[/bold red] {e}")
            return None

        # 3. Load Dataset
        cases = self._load_dataset(spec.dataset_path)
        console.log(f"Loaded {len(cases)} test cases.")

        # 4. Load Prompts
        system_template_str = self._load_prompt_template(spec.prompt_template_path, "system.md")
        user_template_str = self._load_prompt_template(spec.prompt_template_path, "user.md")
        
        system_template = Template(system_template_str)
        user_template = Template(user_template_str)

        # 5. Initialize Scorer
        scorer = ScorerFactory.get_scorer(spec.scoring.scorer_type)

        # 6. Execute Run
        results = []
        start_time_global = time.time()
        
        with console.status("[bold yellow]Running pipeline...[/bold yellow]", spinner="dots"):
            for case in cases:
                # Render Prompt
                system_prompt = system_template.render() # No vars for now
                user_prompt = user_template.render(input=case.input, constraints=case.constraints)
                
                full_prompt = f"{system_prompt}\n\n{user_prompt}" # Simplification for MVP adapter
                
                # Generate
                start_time_case = time.time()
                
                # Merge CLI kwargs with run_config, CLI takes precedence
                run_params = spec.run_config.model_dump()
                run_params.update(kwargs)
                
                response = adapter.generate(full_prompt, **run_params)
                latency = time.time() - start_time_case
                
                # Score
                score_result = scorer.score(case, response.content)
                
                # Store Result
                results.append(CaseResult(
                    case_id=case.case_id,
                    prompt_render_hash=hashlib.sha256(full_prompt.encode()).hexdigest(),
                    model_output=response.content,
                    scores=score_result,
                    timings={"latency": latency}
                ))

        # 7. Aggregate & Save
        timestamp = datetime.now().isoformat().replace(":", "-")
        run_id = f"{timestamp}_{spec.id}"
        run_dir = os.path.join(self.results_dir, run_id)
        os.makedirs(run_dir, exist_ok=True)

        # Calculate Summary
        total_score = sum(r.scores.score for r in results)
        summary = {
            "total_cases": len(results),
            "mean_score": total_score / len(results) if results else 0,
            "duration": time.time() - start_time_global
        }

        run_result = BenchmarkRunResult(
            run_id=run_id,
            timestamp=timestamp,
            spec=spec,
            run_config=spec.run_config,
            model_info={"provider": model_provider, "model": adapter.model_name},
            cases=results,
            summary=summary
        )

        output_path = os.path.join(run_dir, "result.json")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(run_result.model_dump_json(indent=2))
        
        console.log(f"[bold green]Benchmark completed successfully![/bold green]")
        console.log(f"Results saved to: {output_path}")
        console.print(f"Mean Score: {summary['mean_score']:.2f}")
        
        return run_result
