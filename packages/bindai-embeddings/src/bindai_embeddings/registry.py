from __future__ import annotations

from .provider import EmbeddingProvider


class EmbeddingRegistry:
    _providers: dict[str, type[EmbeddingProvider]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[EmbeddingProvider],
    ):
        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ):
        return cls._providers[name]
