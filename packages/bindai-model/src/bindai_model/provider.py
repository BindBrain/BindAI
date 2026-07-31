from __future__ import annotations

from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str: ...
