import itertools
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any
from rich.console import Console

from .schema import PipelineConfig
from .loader import load_pipeline_config
from .cache import generate_run_fingerprint
from .engine import PipelineEngine # Reuse existing single-run engine logic
from benchmarks.schema import BenchmarkRunResult

console = Console()

class AutoPipeline:
    def __init__(self, config_path: str, base_dir: str = "."):
        self.config = load_pipeline_config(config_path)
        self.engine = PipelineEngine(base_dir=base_dir)
        self.cache_dir = os.path.join(base_dir, ".cache", "runs")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_matrix(self) -> List[Dict[str, Any]]:
        """
        Explodes the configuration into a list of individual run configurations.
        """
        keys = list(self.config.parameters.keys())
        values = list(self.config.parameters.values())
        param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        runs = []
        for benchmark_id in self.config.benchmarks:
            for provider in self.config.providers:
                if provider not in self.config.models:
                    console.print(f"[bold yellow]Warning:[/bold yellow] No models configured for provider {provider}, skipping.")
                    continue
                    
                for model in self.config.models[provider]:
                    if not param_combinations:
                        # Case with no matrix params
                        runs.append({
                            "benchmark": benchmark_id,
                            "provider": provider,
                            "model": model,
                            "params": {}
                        })
                    else:
                        for params in param_combinations:
                            runs.append({
                                "benchmark": benchmark_id,
                                "provider": provider,
                                "model": model,
                                "params": params
                            })
        return runs

    def _check_cache(self, fingerprint: str) -> bool:
        cache_path = os.path.join(self.cache_dir, fingerprint, "result.json")
        return os.path.exists(cache_path)

    def run(self, dry_run: bool = False):
        matrix = self._generate_matrix()
        console.print(f"[bold]Found {len(matrix)} run combinations.[/bold]")
        
        results_summary = {"total": len(matrix), "succeeded": 0, "failed": 0, "cached": 0}
        
        for i, run_config in enumerate(matrix):
            console.rule(f"Run {i+1}/{len(matrix)}")
            
            # 1. Resolve Spec (needed for fingerprint)
            specs = self.engine.list_benchmarks()
            spec = next((s for s in specs if s.id == run_config["benchmark"]), None)
            if not spec:
                console.print(f"[bold red]Benchmark {run_config['benchmark']} not found![/bold red]")
                results_summary["failed"] += 1
                continue

            # 2. Fingerprint
            # MVP: Assuming dataset_hash is in spec or we calculate it. 
            # For now using spec.dataset_path as proxy if hash missing
            dataset_hash = spec.dataset_hash or spec.dataset_path 
            
            fingerprint = generate_run_fingerprint(
                spec.id, spec.version, dataset_hash, spec.prompt_version,
                run_config["provider"], run_config["model"], run_config["params"]
            )
            
            console.print(f"Run Config: {run_config}")
            console.print(f"Fingerprint: {fingerprint}")

            # 3. Cache Check
            if self.config.run_options.cache_policy != "disable":
                if self._check_cache(fingerprint):
                    console.print("[bold green]Cache Hit! Skipping execution.[/bold green]")
                    results_summary["cached"] += 1
                    results_summary["succeeded"] += 1
                    
                    if self.config.run_options.cache_policy == "use":
                        continue
            
            if dry_run:
                console.print("[dim]Dry run: execution skipped.[/dim]")
                continue

            # 4. Execute
            try:
                # We need to adapt PipelineEngine.run_benchmark to accept output path or return result
                # For now, we'll let it save to standard runs/ dir, and we might link it to cache
                # Or better, we intercept the result saving in a real implementation.
                # For MVP, we call the engine and then manually handle caching "after the fact" logic 
                # or rely on engine to return the result object if we modify it.
                
                # Let's modify engine to return the result object to us
                # But since I can't easily modify the engine signature in this turn without breaking CLI? 
                # Actually I can, CLI ignores return value.
                
                # NOTE: I need to modify engine.py to return the BenchmarkRunResult
                run_result = self.engine.run_benchmark(
                    run_config["benchmark"], 
                    run_config["provider"], 
                    run_config["model"], 
                    **run_config["params"]
                )
                
                if run_result:
                    # Save to Cache
                    run_cache_dir = os.path.join(self.cache_dir, fingerprint)
                    os.makedirs(run_cache_dir, exist_ok=True)
                    with open(os.path.join(run_cache_dir, "result.json"), "w", encoding="utf-8") as f:
                        f.write(run_result.model_dump_json(indent=2))
                    
                    results_summary["succeeded"] += 1
                else:
                     results_summary["failed"] += 1

            except Exception as e:
                console.print(f"[bold red]Run Failed:[/bold red] {e}")
                results_summary["failed"] += 1
                if self.config.run_options.fail_fast:
                    console.print("[bold red]Fail-fast enabled. Aborting pipeline.[/bold red]")
                    break
        
        console.rule("Pipeline Summary")
        console.print(results_summary)
