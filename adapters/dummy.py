from .base import BaseModelAdapter, ModelResponse
import time

class DummyAdapter(BaseModelAdapter):
    """
    A dummy model adapter for testing the pipeline without external API calls.
    It returns deterministic responses based on the input.
    """

    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """
        Generates a dummy response.
        """
        # Simulate network latency
        time.sleep(0.1)

        # Deterministic simple logic for testing
        response_content = f"Dummy response to: {prompt[:50]}..."
        
        # If the prompt contains "factorial", return the expected python snippet for the test case
        if "factorial" in prompt:
            response_content = "def factorial(n):"
        elif "isPalindrome" in prompt:
             response_content = "function isPalindrome(str) {"

        return ModelResponse(
            content=response_content,
            raw_output={"dummy": True},
            metadata={
                "finish_reason": "stop",
                "usage": {"prompt_tokens": len(prompt), "completion_tokens": len(response_content)}
            },
            model_name=self.model_name
        )
