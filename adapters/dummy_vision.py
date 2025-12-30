from .base import BaseModelAdapter, ModelResponse, BaseVisionAdapter, ImageResult
import time

class DummyVisionAdapter(BaseVisionAdapter):
    """
    A dummy vision adapter for testing.
    """
    
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        return ModelResponse(content="Dummy Vision Adapter text response", model_name=self.model_name)

    def render_image(self, prompt: str, **params) -> ImageResult:
        # Minimal 1x1 transparent PNG
        dummy_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        return ImageResult(
            image_bytes=dummy_png,
            image_format="png",
            width=params.get("width", 1024),
            height=params.get("height", 1024),
            seed=params.get("seed", 12345),
            provider="dummy_provider",
            model=self.model_name,
            latency_ms=10.0
        )
