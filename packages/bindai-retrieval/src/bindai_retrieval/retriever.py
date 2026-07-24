from __future__ import annotations

from .provider import RetrieverProvider
from .registry import RetrievalRegistry
from .query import RetrievalQuery
from .result import RetrievalResult


class Retriever:
    """
    High-level retriever facade.
    """

    def __init__(
        self,
        provider: RetrieverProvider | str,
        **kwargs,
    ):

        if isinstance(provider, str):
            provider = RetrievalRegistry.provider(
                provider,
            )(**kwargs)

        self.provider = provider

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:

        return self.provider.retrieve(
            RetrievalQuery(
                text=query,
                limit=top_k,
            )
        )