from __future__ import annotations

from abc import ABC, abstractmethod
from bindai_model.result import ModelResult

class ModelProvider(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> ModelResult: ...
