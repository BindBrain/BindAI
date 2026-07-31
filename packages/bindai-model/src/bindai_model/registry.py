from __future__ import annotations

from .provider import ModelProvider


class ModelRegistry:
    _providers: dict[
        str,
        type[ModelProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider,
    ):
        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ):
        return cls._providers[name]
