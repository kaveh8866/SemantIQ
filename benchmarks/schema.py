from typing import List, Dict, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class BenchmarkCategory(str, Enum):
    CODE_WRITER = "code_writer"
    REASONING = "reasoning"
    RETRIEVAL = "retrieval"
    GENERAL = "general"

class RunParameter(BaseModel):
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1024, gt=0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    seed: Optional[int] = None

class ScoringConfig(BaseModel):
    scorer_type: str = Field(..., description="Type of scorer to use (e.g., 'exact_match', 'heuristic')")
    metrics: List[str] = Field(..., description="List of metrics to calculate")

class BenchmarkSpec(BaseModel):
    """
    Defines the configuration for a benchmark.
    This schema ensures reproducibility and standardization.
    """
    id: str = Field(..., pattern=r"^[a-z0-9_-]+$", description="Unique, machine-readable ID")
    name: str = Field(..., description="Human-readable name")
    category: BenchmarkCategory
    version: str = Field(..., description="Semantic version of the benchmark")
    dataset_path: str = Field(..., description="Path to the dataset file (relative to datasets/)")
    dataset_hash: Optional[str] = Field(None, description="SHA256 hash of the dataset file for verification")
    prompt_template_path: str = Field(..., description="Path to the prompt template directory (relative to prompts/)")
    prompt_version: str = Field(..., description="Version of the prompt template to use")
    run_config: RunParameter = Field(default_factory=RunParameter)
    scoring: ScoringConfig
    output_artifact_format: str = Field("json", description="Format of the result file")

class TestCase(BaseModel):
    """
    Represents a single test case from a dataset.
    """
    case_id: str = Field(..., description="Unique ID for the test case")
    input: str = Field(..., description="The input/question for the model")
    expected: Optional[Union[str, List[str], Dict[str, Any]]] = Field(None, description="Expected output for scoring")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context (difficulty, tags, etc.)")
    constraints: List[str] = Field(default_factory=list, description="Execution constraints")

class ScoreResult(BaseModel):
    score: float = Field(..., description="Numerical score (0.0 to 1.0)")
    metrics: Dict[str, Any] = Field(..., description="Detailed metric values")
    details: Optional[str] = Field(None, description="Explanation or reasoning for the score")

class CaseResult(BaseModel):
    case_id: str
    prompt_render_hash: str
    model_output: str
    scores: ScoreResult
    timings: Optional[Dict[str, float]] = None

class BenchmarkRunResult(BaseModel):
    """
    The final output artifact of a benchmark run.
    """
    run_id: str
    timestamp: str
    spec: BenchmarkSpec
    run_config: RunParameter
    model_info: Dict[str, Any]
    cases: List[CaseResult]
    summary: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Environment metadata (git, python, etc.)")
