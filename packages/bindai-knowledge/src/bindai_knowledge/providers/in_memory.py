from __future__ import annotations

from ..document import KnowledgeDocument
from ..provider import KnowledgeProvider
from ..result import KnowledgeResult


class InMemoryKnowledgeProvider(KnowledgeProvider):

    def __init__(self):

        self._documents: dict[
            str,
            KnowledgeDocument,
        ] = {}

    def add(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeResult:

        self._documents[
            document.id
        ] = document

        return KnowledgeResult(
            success=True,
            value=document,
        )

    def get(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        return KnowledgeResult(
            success=True,
            value=self._documents.get(
                document_id,
            ),
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> KnowledgeResult:

        words = [
            word.strip(".,?!")
            for word in query.lower().split()
            if len(word) > 2
        ]

        results = []

        for document in self._documents.values():

            haystack = (
                document.title
                + " "
                + document.content
            ).lower()

            score = sum(
                word in haystack
                for word in words
            )

            if score > 0:

                results.append(
                    (score, document),
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return KnowledgeResult(
            success=True,
            value=[
                document
                for _, document in results[:limit]
            ],
        )

    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        self._documents.pop(
            document_id,
            None,
        )

        return KnowledgeResult(
            success=True,
        )

    def clear(
        self,
    ) -> KnowledgeResult:

        self._documents.clear()

        return KnowledgeResult(
            success=True,
        )