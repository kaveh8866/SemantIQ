from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ModelResponse(BaseModel):
    """
    Standardized response from a model adapter.
    """
    content: str = Field(..., description="The raw text output from the model.")
    raw_output: Any = Field(None, description="The original raw response object from the provider.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Usage stats, finish reason, etc.")
    model_name: str = Field(..., description="The name of the model that generated this response.")

class ImageResult(BaseModel):
    """
    Standardized result from a vision model adapter.
    """
    image_bytes: Optional[bytes] = Field(None, description="The raw image bytes.")
    image_path: Optional[str] = Field(None, description="Path to the saved image file.")
    image_format: str = Field(..., description="Image format (png, jpg).")
    width: int = Field(..., description="Image width.")
    height: int = Field(..., description="Image height.")
    seed: Optional[int] = Field(None, description="Seed used for generation, if supported.")
    provider: str = Field(..., description="Provider name.")
    model: str = Field(..., description="Model name.")
    request_id: Optional[str] = Field(None, description="Provider request ID.")
    latency_ms: Optional[float] = Field(None, description="Generation latency in milliseconds.")

class BaseModelAdapter(ABC):
    """
    Abstract base class for all model adapters.
    Ensures a consistent interface for the pipeline.
    """

    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """
        Send a prompt to the model and return a standardized response.
        
        Args:
            prompt: The input text prompt.
            **kwargs: Additional provider-specific parameters (temperature, max_tokens, etc.)
            
        Returns:
            ModelResponse: The standardized output.
        """
        pass

class BaseVisionAdapter(BaseModelAdapter):
    """
    Abstract base class for vision model adapters (T2I).
    """

    @abstractmethod
    def render_image(self, prompt: str, **params) -> ImageResult:
        """
        Render an image from a prompt.

        Args:
            prompt: The input text prompt.
            **params: Normalized rendering parameters.

        Returns:
            ImageResult: The standardized image result.
        """
        pass
