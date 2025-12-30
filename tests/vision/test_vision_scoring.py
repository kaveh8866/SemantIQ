import pytest
import os
import json
import shutil
from unittest.mock import MagicMock, patch
from benchmarks.vision.scoring import VisionScoringEngine, ScoreResult, DeterministicMockScorer, RunReport

# --- Fixtures ---

@pytest.fixture
def mock_run_data(tmp_path):
    run_id = "test_run_scoring"
    run_dir = tmp_path / "runs" / "vision" / run_id
    images_dir = run_dir / "images"
    metadata_dir = run_dir / "metadata"
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Create mock images
    (images_dir / "p1_hash1.png").touch()
    (images_dir / "p2_hash2.png").touch()
    
    # Create metadata
    image_metadata = [
        {
            "prompt_id": "p1",
            "prompt_hash": "hash1",
            "category_id": "sof",
            "provider": "dummy",
            "model": "test-model"
        },
        {
            "prompt_id": "p2",
            "prompt_hash": "hash2",
            "category_id": "moc",
            "provider": "dummy",
            "model": "test-model"
        }
    ]
    
    with open(metadata_dir / "IMAGE_METADATA.json", "w") as f:
        json.dump(image_metadata, f)
        
    with open(metadata_dir / "RUN_METADATA.json", "w") as f:
        json.dump({"provider": "dummy", "model": "test-model"}, f)
        
    # Mock Reports dir
    reports_dir = tmp_path / "reports" / "vision" / "runs" / run_id
    os.makedirs(reports_dir, exist_ok=True)
        
    return str(tmp_path), run_id

# --- Tests ---

def test_deterministic_scorer():
    scorer = DeterministicMockScorer("test_rubric")
    
    # Same input -> same score
    s1 = scorer.score("path/to/img1.png", {})
    s2 = scorer.score("path/to/img1.png", {})
    assert s1 == s2
    
    # Different input -> likely different score (or at least valid float)
    s3 = scorer.score("path/to/img2.png", {})
    assert isinstance(s3, float)
    assert 0.0 <= s3 <= 1.0

def test_scoring_engine_mapping():
    # Test loading mapping
    engine = VisionScoringEngine() # Should load real mapping from disk if available, or fail
    # We can patch _load_mapping if we want to test isolation, but integration test is good too
    assert "sof" in engine.mapping
    assert "object_presence" in engine.mapping["sof"]["primary_rubrics"]

def test_score_image():
    engine = VisionScoringEngine()
    
    # Mock image path
    img_path = "test_image.png"
    prompt_data = {"prompt_id": "p1", "category_id": "sof"}
    
    result = engine.score_image(img_path, prompt_data)
    
    assert isinstance(result, ScoreResult)
    assert result.prompt_id == "p1"
    assert result.overall_score >= 0.0
    assert "object_presence" in result.scores

def test_score_run(mock_run_data):
    base_path, run_id = mock_run_data
    
    # Patch os.path.join or use chdir to trick the engine into looking at tmp_path
    # Since engine uses relative "runs/" paths, we need to run from tmp_path or patch paths
    
    original_cwd = os.getcwd()
    os.chdir(base_path)
    
    try:
        # Create mapping file in tmp_path/benchmarks/vision if engine loads it relatively
        os.makedirs("benchmarks/vision", exist_ok=True)
        shutil.copy(os.path.join(original_cwd, "benchmarks/vision/scoring_mapping.yaml"), "benchmarks/vision/scoring_mapping.yaml")
        
        engine = VisionScoringEngine()
        report = engine.score_run(run_id)
        
        assert isinstance(report, RunReport)
        assert report.run_id == run_id
        assert report.overall_score >= 0.0
        assert "sof" in report.category_summaries
        assert "moc" in report.category_summaries
        
        # Check files created
        assert os.path.exists(f"reports/vision/runs/{run_id}/overall_summary.json")
        assert os.path.exists(f"reports/vision/runs/{run_id}/prompt_scores.json")
        
    finally:
        os.chdir(original_cwd)

def test_rubric_mapping_validity():
    # Ensure all rubrics in mapping have a corresponding scorer in engine
    engine = VisionScoringEngine()
    
    for cat_id, mapping in engine.mapping.items():
        rubrics = mapping.get("primary_rubrics", []) + mapping.get("secondary_rubrics", [])
        for r in rubrics:
            assert r in engine.scorers, f"Rubric {r} in category {cat_id} has no implemented scorer"

