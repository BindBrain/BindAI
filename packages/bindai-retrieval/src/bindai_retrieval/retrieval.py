from __future__ import annotations

from .provider import RetrieverProvider
from .registry import RetrievalRegistry
from .query import RetrievalQuery
from .result import RetrievalResult


class Retrieval:
    """
    High-level retrieval facade.
    """

    def __init__(
        self,
        provider: RetrieverProvider | str,
        **kwargs,
    ):

        if isinstance(
            provider,
            str,
        ):
            provider = (
                RetrievalRegistry.provider(
                    provider,
                )
            )(**kwargs)

        self.provider = provider

    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:

        return self.provider.retrieve(
            query,
        )