from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from ..document import KnowledgeDocument
from .base import DocumentLoader


class _HTMLTextExtractor(HTMLParser):
    """
    Simple HTML -> text extractor using the Python standard library.
    """

    def __init__(self):
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str):
        text = data.strip()

        if text:
            self._parts.append(text)

    @property
    def text(self) -> str:
        return " ".join(self._parts)


class HTMLLoader(DocumentLoader):
    """
    Loads an HTML document and extracts its visible text.
    """

    def __init__(
        self,
        path: str,
    ):
        self.path = Path(path)

    def load(
        self,
    ) -> list[KnowledgeDocument]:

        parser = _HTMLTextExtractor()

        parser.feed(
            self.path.read_text(
                encoding="utf-8",
            )
        )

        parser.close()

        return [
            KnowledgeDocument(
                id=self.path.stem,
                title=self.path.name,
                content=parser.text,
                metadata={
                    "path": str(self.path),
                    "extension": self.path.suffix,
                },
            )
        ]