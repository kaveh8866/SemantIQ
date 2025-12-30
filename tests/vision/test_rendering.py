import os
import shutil
import pytest
import json
from benchmarks.vision.rendering import VisionRenderer, RenderParams
from adapters.dummy_vision import DummyVisionAdapter

# Mock prompt
class MockPrompt:
    prompt_id = "test_prompt_01"
    prompt_text = "A test prompt"
    category_id = "test_cat"
    archetype_id = "test_arch"

def test_prompt_hashing():
    adapter = DummyVisionAdapter(model_name="test")
    renderer = VisionRenderer(adapter=adapter, run_id="test_run_hash")
    
    params1 = RenderParams(width=1024, height=1024, seed=42)
    params2 = RenderParams(width=1024, height=1024, seed=42)
    params3 = RenderParams(width=512, height=512, seed=42)
    
    hash1 = renderer.generate_prompt_hash("A test prompt", "test_prompt_01", params1)
    hash2 = renderer.generate_prompt_hash("A test prompt", "test_prompt_01", params2)
    hash3 = renderer.generate_prompt_hash("A test prompt", "test_prompt_01", params3)
    
    assert hash1 == hash2
    assert hash1 != hash3
    
    # Cleanup
    if os.path.exists(renderer.base_dir):
        shutil.rmtree(renderer.base_dir)

def test_image_capture():
    adapter = DummyVisionAdapter(model_name="test")
    run_id = "test_run_capture"
    renderer = VisionRenderer(adapter=adapter, run_id=run_id)
    
    prompt = MockPrompt()
    params = RenderParams(seed=123)
    
    result = renderer.render_prompt(prompt, params)
    
    # Check result
    assert result.image_path is not None
    assert os.path.exists(result.image_path)
    
    # Check metadata
    meta_path = os.path.join(renderer.metadata_dir, "IMAGE_METADATA.json")
    assert os.path.exists(meta_path)
    
    with open(meta_path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["prompt_id"] == "test_prompt_01"
        assert data[0]["prompt_hash"] == renderer.generate_prompt_hash(prompt.prompt_text, prompt.prompt_id, params)

    # Cleanup
    if os.path.exists(renderer.base_dir):
        shutil.rmtree(renderer.base_dir)
