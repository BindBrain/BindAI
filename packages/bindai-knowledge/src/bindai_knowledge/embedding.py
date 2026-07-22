from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> list[float]: ...


class Embedding:
    def __init__(
        self,
        provider: EmbeddingProvider,
    ):
        self.provider = provider

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed(
            text,
        )
