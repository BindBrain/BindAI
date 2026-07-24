from __future__ import annotations

from bindai_memory import Memory

from bindai_retrieval.provider import RetrieverProvider
from bindai_retrieval.query import RetrievalQuery
from bindai_retrieval.result import RetrievalResult


class MemoryRetrieverProvider(RetrieverProvider):

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