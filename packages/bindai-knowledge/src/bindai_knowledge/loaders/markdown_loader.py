from pathlib import Path

from ..document import KnowledgeDocument
from .base import DocumentLoader


class MarkdownLoader(DocumentLoader):

    def __init__(
        self,
        path: str,
    ):
        self.path = Path(path)

    def load(
        self,
    ) -> list[KnowledgeDocument]:

        content = self.path.read_text(
            encoding="utf-8",
        )

        return [
            KnowledgeDocument(
                id=self.path.stem,
                title=self.path.name,
                content=content,
                metadata={
                    "path": str(self.path),
                    "extension": self.path.suffix,
                },
            )
        ]