from __future__ import annotations

from typing import Type

from .provider import EmbeddingProvider


class EmbeddingRegistry:

    _providers: dict[str, Type[EmbeddingProvider]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: Type[EmbeddingProvider],
    ):
        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ):
        return cls._providers[name]