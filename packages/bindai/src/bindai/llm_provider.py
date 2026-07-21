from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .llm_result import LLMResult


class LLMProvider(ABC):
    """
    Base class for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> LLMResult:
        ...