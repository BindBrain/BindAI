from __future__ import annotations

import re

from .document import KnowledgeDocument
from .reranker_base import Reranker


class LexicalReranker(Reranker):
    """
    Reranks knowledge documents using query-term overlap.
    """

    def rerank(
        self,
        query: str,
        documents: list[KnowledgeDocument],
    ) -> list[KnowledgeDocument]:

        query_terms = self._terms(query)

        if not query_terms:
            return list(documents)

        scored = []

        for index, document in enumerate(documents):
            document_terms = self._terms(f"{document.title} {document.content}")

            overlap = len(query_terms & document_terms)

            score = overlap / len(query_terms)

            scored.append(
                (
                    score,
                    index,
                    document,
                )
            )

        scored.sort(
            key=lambda item: (
                item[0],
                -item[1],
            ),
            reverse=True,
        )

        return [document for _, _, document in scored]

    @staticmethod
    def _terms(text: str) -> set[str]:
        return set(
            re.findall(
                r"\b\w+\b",
                text.lower(),
            )
        )
