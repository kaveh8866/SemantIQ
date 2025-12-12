from __future__ import annotations

from abc import ABC, abstractmethod

from semantiq.schemas import ModelParameters, UsageMeta


class LLMClient(ABC):
    provider: str
    model_name: str

    @abstractmethod
    def generate(self, prompt: str, parameters: ModelParameters) -> tuple[str, dict | None, UsageMeta | None]:
        raise NotImplementedError