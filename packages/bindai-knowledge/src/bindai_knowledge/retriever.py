from __future__ import annotations

from bindai_retrieval import Retriever


class KnowledgeRetriever:

    def __init__(
        self,
        retriever: Retriever,
    ):
        self.retriever = retriever

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ):

        return self.retriever.retrieve(
            query,
            top_k=limit,
        )