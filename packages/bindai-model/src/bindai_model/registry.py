from __future__ import annotations

from typing import Type

from .provider import ModelProvider


class ModelRegistry:

    _providers: dict[
        str,
        Type[ModelProvider],
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