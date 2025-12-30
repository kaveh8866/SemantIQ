from typing import Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.settings import settings
from adapters.base import BaseModelAdapter, ModelResponse

class OpenRouterAdapter(BaseModelAdapter):
    """
    Adapter for OpenRouter API.
    Compatible with OpenAI's Chat Completions API but allows for provider routing.
    """
    
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name, **kwargs)
        self.api_key = settings.OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
        self.base_url = settings.OPENROUTER_BASE_URL
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://semantiq.benchmarks", # Required by OpenRouter
                "X-Title": "SemantIQ Benchmarks", # Optional
            },
            timeout=kwargs.get("timeout", 30.0)
        )

    @retry(
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """
        Generates a response using OpenRouter.
        """
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.0),
            "max_tokens": kwargs.get("max_tokens", 1000),
        }
        
        # Pass through other kwargs that might be relevant for OpenRouter
        # (e.g. top_p, repetition_penalty if supported by the underlying model)
        
        try:
            response = self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            # OpenRouter response structure is similar to OpenAI
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            
            return ModelResponse(
                content=content,
                raw_output=data,
                metadata={
                    "usage": usage,
                    "finish_reason": data["choices"][0].get("finish_reason"),
                    "request_id": data.get("id"),
                    "provider": "openrouter"
                },
                model_name=self.model_name
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                pass # Tenacity handles this
            raise e
