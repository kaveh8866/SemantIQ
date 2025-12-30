from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field

class RunOptions(BaseModel):
    parallelism: bool = False
    max_workers: int = 1
    fail_fast: bool = False
    cache_policy: str = Field("use", pattern="^(use|refresh|disable)$")

class OutputOptions(BaseModel):
    base_dir: str = "runs"
    naming_scheme: str = "{timestamp}_{benchmark_id}_{provider}_{model}"

class PipelineConfig(BaseModel):
    benchmarks: List[str]
    providers: List[str]
    models: Dict[str, List[str]] # Provider -> List of Models
    parameters: Dict[str, List[Union[str, int, float, bool]]] # Matrix parameters
    run_options: RunOptions = Field(default_factory=RunOptions)
    output_options: OutputOptions = Field(default_factory=OutputOptions)
