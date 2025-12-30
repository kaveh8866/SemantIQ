from typing import Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.settings import settings
from adapters.base import BaseModelAdapter, ModelResponse

class OpenAIAdapter(BaseModelAdapter):
    """
    Adapter for OpenAI's Chat Completions API.
    """
    
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name, **kwargs)
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.base_url = kwargs.get("base_url", "https://api.openai.com/v1")
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
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
        Generates a response using OpenAI's API.
        """
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.0),
            "max_tokens": kwargs.get("max_tokens", 1000),
        }
        
        # Support for seed if provided
        if "seed" in kwargs:
            payload["seed"] = kwargs["seed"]

        try:
            response = self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            
            return ModelResponse(
                content=content,
                raw_output=data,
                metadata={
                    "usage": usage,
                    "finish_reason": data["choices"][0].get("finish_reason"),
                    "request_id": data.get("id"),
                    "provider": "openai"
                },
                model_name=self.model_name
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                # In a real scenario, we might want to respect Retry-After header
                # For now, tenacity handles the backoff
                pass
            raise e
