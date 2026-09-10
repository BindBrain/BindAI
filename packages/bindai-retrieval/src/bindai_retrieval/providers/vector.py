from __future__ import annotations

from bindai_memory import Memory

from ..provider import RetrieverProvider
from ..query import RetrievalQuery
from ..result import RetrievalResult


class VectorRetrieverProvider(RetrieverProvider):
    def __init__(
        self,
        memory: Memory,
    ):
        self.memory = memory

    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:

        documents = self.memory.search(
            query=query.text,
            namespace=query.namespace,
            limit=query.limit,
            metadata=query.metadata,
        )

        return RetrievalResult(
            success=True,
            documents=documents,
        )
