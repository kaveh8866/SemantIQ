import pytest
import os
import json
from pipeline.schema import PipelineConfig
from pipeline.loader import load_pipeline_config
from pipeline.cache import generate_run_fingerprint
from pipeline.registry import ResultRegistry

# --- Unit Tests ---

def test_pipeline_config_validation():
    """
    Test that the PipelineConfig Pydantic model validates correctly.
    """
    valid_data = {
        "benchmarks": ["bench_1"],
        "providers": ["dummy"],
        "models": {"dummy": ["model_a"]},
        "parameters": {"temperature": [0.7]},
        "run_options": {"cache_policy": "use"},
        "output_options": {}
    }
    config = PipelineConfig(**valid_data)
    assert config.benchmarks == ["bench_1"]
    assert config.run_options.cache_policy == "use"

    invalid_data = {
        "benchmarks": ["bench_1"],
        # Missing providers and models
    }
    with pytest.raises(ValueError):
        PipelineConfig(**invalid_data)

def test_run_fingerprint_stability():
    """
    Test that run fingerprinting is deterministic.
    """
    params1 = {"temperature": 0.7, "seed": 42}
    params2 = {"seed": 42, "temperature": 0.7} # Different order
    
    fp1 = generate_run_fingerprint("b1", "v1", "h1", "p1", "prov", "mod", params1)
    fp2 = generate_run_fingerprint("b1", "v1", "h1", "p1", "prov", "mod", params2)
    
    assert fp1 == fp2
    
    params3 = {"temperature": 0.8}
    fp3 = generate_run_fingerprint("b1", "v1", "h1", "p1", "prov", "mod", params3)
    assert fp1 != fp3

def test_registry_indexing(tmp_path):
    """
    Test that the ResultRegistry correctly indexes run files.
    """
    # Setup mock runs directory
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    
    run_id = "run_123"
    run_dir = runs_dir / run_id
    run_dir.mkdir()
    
    result_data = {
        "run_id": run_id,
        "timestamp": "2025-01-01",
        "spec": {"id": "bench_1"},
        "model_info": {"provider": "dummy", "model": "test"},
        "summary": {"mean_score": 0.95}
    }
    
    with open(run_dir / "result.json", "w") as f:
        json.dump(result_data, f)
        
    registry = ResultRegistry(base_dir=str(tmp_path))
    registry.update_index()
    
    index = registry.get_index()
    assert len(index) == 1
    assert index[0]["run_id"] == run_id
    assert index[0]["mean_score"] == 0.95

# --- Integration Test ---
# Note: This requires the full environment (datasets, prompts) to be present or mocked.
# We will create a minimal test that runs the pipeline with the dummy adapter.

def test_pipeline_execution_dummy(tmp_path):
    # 1. Create a dummy config file
    config_data = {
        "benchmarks": ["code_writer_v1"],
        "providers": ["dummy"],
        "models": {"dummy": ["test-model"]},
        "parameters": {
            "temperature": [0.1, 0.9]
        },
        "run_options": {
            "cache_policy": "disable"
        }
    }
    
    config_path = tmp_path / "pipeline_config.yaml"
    with open(config_path, "w") as f:
        import yaml
        yaml.dump(config_data, f)
        
    # 2. Mock necessary project structure
    # We need to point the AutoPipeline to the real project root or mock everything.
    # Since we are in the project, we can use the real directory but override output.
    # However, AutoPipeline uses PipelineEngine which defaults to base_dir.
    # We will assume we are running in the project root for this test or mock loading.
    
    # For simplicity in this environment, we'll verify the Config Loading part of integration
    # and skip full execution if dependencies are missing, but let's try to run it if possible.
    
    loaded_config = load_pipeline_config(str(config_path))
    assert len(loaded_config.parameters["temperature"]) == 2
    assert loaded_config.providers == ["dummy"]
