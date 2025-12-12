from __future__ import annotations

from abc import ABC, abstractmethod

from semantiq.schemas import ModelAnswer, ModelConfig


class BaseModelProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, prompt: str, config: ModelConfig) -> ModelAnswer:  # noqa: D401
        raise NotImplementedError