from typing import Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.settings import settings
from adapters.base import BaseModelAdapter, ModelResponse

class MarberAdapter(BaseModelAdapter):
    """
    Adapter for Marber API (Gateway/Proxy).
    """
    
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name, **kwargs)
        self.api_key = settings.MARBER_API_KEY
        self.base_url = settings.MARBER_API_URL
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"
            
        self.client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
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
        Generates a response using Marber API.
        Payload structure assumed to be model-agnostic but similar to common standards.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt, # Assuming Marber accepts a simple prompt or messages
            # If Marber follows OpenAI chat format, we might need to wrap in messages
            # For now, assuming a generic payload based on prompt description
            "messages": [{"role": "user", "content": prompt}], 
            "parameters": {
                "temperature": kwargs.get("temperature", 0.0),
                "max_tokens": kwargs.get("max_tokens", 1000),
            }
        }
        
        try:
            # Assuming Marber endpoint is /chat/completions or similar
            # Adjusting to generic /generate or similar if specified. 
            # Prompt doesn't specify Marber endpoint structure, assuming standard /v1/chat/completions compatible or custom
            # Prompt says: "payload: prompt + parameters + requested model"
            
            # Let's assume a generic endpoint since it's a proxy
            response = self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Normalize Response: text + raw + usage
            # Assuming standard response format or mapping it
            content = ""
            if "choices" in data and len(data["choices"]) > 0:
                 content = data["choices"][0]["message"]["content"]
            elif "text" in data:
                 content = data["text"]
            
            usage = data.get("usage", {})
            
            return ModelResponse(
                content=content,
                raw_output=data,
                metadata={
                    "usage": usage,
                    "provider": "marber",
                    "request_id": data.get("id")
                },
                model_name=self.model_name
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                pass 
            raise e
