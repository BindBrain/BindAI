from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ModelProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        ...