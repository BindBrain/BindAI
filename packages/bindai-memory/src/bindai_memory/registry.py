from __future__ import annotations

from typing import Type

from .provider import MemoryProvider


class MemoryRegistry:
    """
    Registry of available memory providers.
    """

    _providers: dict[
        str,
        Type[MemoryProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: Type[MemoryProvider],
    ) -> None:

        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ) -> Type[MemoryProvider]:

        try:
            return cls._providers[name]

        except KeyError as exc:
            raise ValueError(f"Unknown memory provider '{name}'.") from exc

    @classmethod
    def providers(
        cls,
    ) -> dict[str, Type[MemoryProvider]]:

        return dict(cls._providers)
