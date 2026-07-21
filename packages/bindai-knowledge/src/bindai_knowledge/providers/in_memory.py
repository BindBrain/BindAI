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

    def add_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> KnowledgeResult:

        for document in documents:
            self._documents[
                document.id
            ] = document

        return KnowledgeResult(
            success=True,
            value=documents,
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
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        result = self.search_with_scores(
            query=query,
            limit=limit,
            filters=filters,
        )

        return KnowledgeResult(
            success=result.success,
            value=[
                document
                for _, document in result.value
            ],
        )

    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        query = query.strip().lower()

        words = [
            word.strip(".,?!")
            for word in query.split()
            if len(word) > 2
        ]

        results: list[
            tuple[int, KnowledgeDocument]
        ] = []

        for document in self._documents.values():

            if filters:

                metadata = document.metadata or {}

                if not all(
                    metadata.get(key) == value
                    for key, value in filters.items()
                ):
                    continue

            title = document.title.lower()
            content = document.content.lower()

            metadata_text = " ".join(
                str(value)
                for value in (document.metadata or {}).values()
            ).lower()

            score = 0

            if query:

                if query in title:
                    score += 10

                if query in content:
                    score += 5

            for word in words:

                if word in title:
                    score += 5
                    score += title.count(word)

                if word in content:
                    score += 2
                    score += content.count(word)

                if word in metadata_text:
                    score += 1

            if score > 0:

                results.append(
                    (
                        score,
                        document,
                    )
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return KnowledgeResult(
            success=True,
            value=results[:limit],
        )

    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        return self.search(
            query=query,
            limit=limit,
            filters=filters,
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