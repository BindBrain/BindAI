from __future__ import annotations

import json
from pathlib import Path

from ..document import KnowledgeDocument
from ..result import KnowledgeResult
from .in_memory import InMemoryKnowledgeProvider


class JsonKnowledgeProvider(InMemoryKnowledgeProvider):
    """
    Persistent knowledge provider backed by a JSON file.
    """

    def __init__(
        self,
        path: str | Path,
    ):

        super().__init__()

        self.path = Path(path)

        if self.path.exists():
            self._load()

    #
    # Internal helpers
    #

    def _load(self) -> None:

        try:
            data = json.loads(
                self.path.read_text(
                    encoding="utf-8",
                )
            )

        except Exception:
            return

        self._documents.clear()

        for item in data:
            document = KnowledgeDocument(
                id=item["id"],
                title=item["title"],
                content=item["content"],
                metadata=item.get("metadata", {}),
            )

            self._documents[document.id] = document

    def _save(self) -> None:

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = []

        for document in self._documents.values():
            data.append(
                {
                    "id": document.id,
                    "title": document.title,
                    "content": document.content,
                    "metadata": document.metadata,
                }
            )

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    #
    # CRUD
    #

    def add(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeResult:

        result = super().add(document)

        self._save()

        return result

    def add_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> KnowledgeResult:

        result = super().add_many(documents)

        self._save()

        return result

    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        result = super().delete(document_id)

        self._save()

        return result

    def clear(
        self,
    ) -> KnowledgeResult:

        result = super().clear()

        self._save()

        return result

    #
    # Searching
    #

    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        return super().search(
            query=query,
            limit=limit,
            filters=filters,
        )

    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        return super().search_with_scores(
            query=query,
            limit=limit,
            filters=filters,
        )

    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        return super().hybrid_search(
            query=query,
            limit=limit,
            filters=filters,
        )
