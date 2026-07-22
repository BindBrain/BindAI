from __future__ import annotations

from pathlib import Path

from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentLoader
from .text_loader import TextLoader


class DirectoryLoader(DocumentLoader):
    """
    Loads all supported documents from a directory.
    """

    def __init__(
        self,
        path: str,
        recursive: bool = True,
    ):
        self.path = Path(path)
        self.recursive = recursive

    def load(
        self,
    ) -> list[KnowledgeDocument]:

        documents: list[KnowledgeDocument] = []

        pattern = "**/*" if self.recursive else "*"

        for file in self.path.glob(pattern):
            if not file.is_file():
                continue

            if file.suffix.lower() != ".txt":
                continue

            documents.extend(
                TextLoader(
                    str(file),
                ).load()
            )

        return documents
