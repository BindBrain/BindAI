from typing import Type

from .provider import RetrieverProvider


class RetrievalRegistry:

    _providers: dict[
        str,
        Type[RetrieverProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: Type[RetrieverProvider],
    ) -> None:

        cls._providers[name] = provider

    @classmethod
    def provider(
        cls,
        name: str,
    ) -> Type[RetrieverProvider]:

        try:
            return cls._providers[name]

        except KeyError as exc:
            raise ValueError(
                f"Unknown retriever provider '{name}'."
            ) from exc

    @classmethod
    def providers(
        cls,
    ) -> dict[str, Type[RetrieverProvider]]:

        return dict(cls._providers)


#
# Built-in providers
#

from .providers.memory import MemoryRetrieverProvider
from .providers.vector import VectorRetrieverProvider
from .providers.bm25 import BM25RetrieverProvider
from .providers.hybrid import HybridRetrieverProvider

RetrievalRegistry.register(
    "memory",
    MemoryRetrieverProvider,
)

RetrievalRegistry.register(
    "vector",
    VectorRetrieverProvider,
)

RetrievalRegistry.register(
    "bm25",
    BM25RetrieverProvider,
)

RetrievalRegistry.register(
    "hybrid",
    HybridRetrieverProvider,
)