import hashlib
import json
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid
from pydantic import BaseModel, Field
from adapters.base import BaseVisionAdapter, ImageResult

# --- 2) Rendering Parameters (Normalized) ---
class RenderParams(BaseModel):
    width: int = Field(1024, description="Image width")
    height: int = Field(1024, description="Image height")
    num_images: int = Field(1, description="Number of images to generate")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    steps: Optional[int] = Field(None, description="Inference steps")
    guidance_scale: Optional[float] = Field(None, description="Guidance scale")
    
    def to_normalized_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, mode='json')

class VisionRunMetadata(BaseModel):
    run_id: str
    timestamp: str
    dataset_version: str
    provider: str
    model: str
    params: Dict[str, Any]

class ImageMetadata(BaseModel):
    prompt_id: str
    prompt_hash: str
    category_id: str
    archetype_id: str
    provider: str
    model: str
    render_params: Dict[str, Any]
    seed_supported: bool
    warnings: List[str] = []
    timestamp: str

class VisionRenderer:
    def __init__(self, adapter: BaseVisionAdapter, run_id: Optional[str] = None):
        self.adapter = adapter
        self.run_id = run_id or f"{datetime.now().strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.base_dir = os.path.join("runs", "vision", self.run_id)
        self.images_dir = os.path.join(self.base_dir, "images")
        self.metadata_dir = os.path.join(self.base_dir, "metadata")
        self._ensure_dirs()
        
    def _ensure_dirs(self):
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)

    # --- 3) Prompt Rendering & Hashing (Critical) ---
    def generate_prompt_hash(self, prompt_text: str, prompt_id: str, params: RenderParams) -> str:
        # prompt_text (exact) + prompt_id + template/version (implicit) + normalized parameters
        
        # Sort keys for consistent JSON serialization
        params_json = json.dumps(params.to_normalized_dict(), sort_keys=True)
        
        content = f"{prompt_text}{prompt_id}{params_json}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def render_prompt(self, prompt: Any, params: RenderParams) -> ImageResult:
        # prompt is expected to be a VisionPrompt object
        
        prompt_text = prompt.prompt_text
        prompt_id = prompt.prompt_id
        
        prompt_hash = self.generate_prompt_hash(prompt_text, prompt_id, params)
        
        # print(f"Rendering {prompt_id} (Hash: {prompt_hash[:8]})...")
        
        try:
            # Call adapter
            start_time = time.time()
            result = self.adapter.render_image(prompt=prompt_text, **params.model_dump())
            
            # --- 4) Image Capture & Storage ---
            # Save image
            filename = f"{prompt_id}_{prompt_hash}.{result.image_format}"
            filepath = os.path.join(self.images_dir, filename)
            
            if result.image_bytes:
                with open(filepath, "wb") as f:
                    f.write(result.image_bytes)
                result.image_path = filepath
            elif result.image_path:
                # If adapter returns path, we might copy it or just use it.
                # Assuming adapter might save to temp.
                # Ideally adapter returns bytes or we handle path copying if needed.
                pass 
                
            # Save Metadata
            img_meta = ImageMetadata(
                prompt_id=prompt_id,
                prompt_hash=prompt_hash,
                category_id=prompt.category_id,
                archetype_id=prompt.archetype_id,
                provider=result.provider,
                model=result.model,
                render_params=params.to_normalized_dict(),
                seed_supported=result.seed is not None,
                warnings=[], 
                timestamp=datetime.now().isoformat()
            )
            
            if params.seed is not None and result.seed is None:
                img_meta.warnings.append("Requested seed was not supported by provider.")
            
            self._append_image_metadata(img_meta)
            
            return result
            
        except Exception as e:
            # Failure handling
            raise e

    def _append_image_metadata(self, meta: ImageMetadata):
        meta_path = os.path.join(self.metadata_dir, "IMAGE_METADATA.json")
        data = []
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        
        data.append(meta.model_dump())
        
        with open(meta_path, "w") as f:
            json.dump(data, f, indent=2)

    def save_run_metadata(self, dataset_version: str):
        meta = VisionRunMetadata(
            run_id=self.run_id,
            timestamp=datetime.now().isoformat(),
            dataset_version=dataset_version,
            provider=self.adapter.model_name,
            model=self.adapter.model_name,
            params={} 
        )
        with open(os.path.join(self.metadata_dir, "RUN_METADATA.json"), "w") as f:
            json.dump(meta.model_dump(), f, indent=2)
