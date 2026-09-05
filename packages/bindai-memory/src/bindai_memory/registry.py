from __future__ import annotations

from .provider import MemoryProvider
from .providers.postgresql import PostgreSQLMemoryProvider

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

        if not name:
            raise ValueError("Provider name cannot be empty.")

        if not issubclass(
            provider,
            MemoryProvider,
        ):
            raise TypeError("Provider must inherit from MemoryProvider.")

        cls._providers[name.strip().lower()] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ) -> type[MemoryProvider]:

        key = name.strip().lower()

        try:
            return cls._providers[key]

        except KeyError as exc:
            raise ValueError(f"Unknown memory provider '{name}'.") from exc

    @classmethod
    def providers(
        cls,
    ) -> dict[str, type[MemoryProvider]]:

        return dict(
            cls._providers,
        )

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:

        cls._providers.pop(
            name.strip().lower(),
            None,
        )

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._providers.clear()


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

MemoryRegistry.register(
	"postgresql", 
	PostgreSQLMemoryProvider
)