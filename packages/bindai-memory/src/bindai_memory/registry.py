from __future__ import annotations

from .provider import MemoryProvider


class MemoryRegistry:
    """
    Registry of available memory providers.
    """

    _providers: dict[
        str,
        type[MemoryProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[MemoryProvider],
    ) -> None:

        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ) -> type[MemoryProvider]:

        try:
            return cls._providers[name]

        except KeyError as exc:
            raise ValueError(f"Unknown memory provider '{name}'.") from exc

    @classmethod
    def providers(
        cls,
    ) -> dict[str, type[MemoryProvider]]:

        return dict(cls._providers)


#
# Built-in providers
#

from .providers.in_memory import InMemoryProvider
from .providers.sqlite import SQLiteMemoryProvider
from .providers.vector_memory import VectorMemoryProvider

MemoryRegistry.register(
    "memory",
    InMemoryProvider,
)

MemoryRegistry.register(
    "sqlite",
    SQLiteMemoryProvider,
)

MemoryRegistry.register(
    "vector",
    VectorMemoryProvider,
)
