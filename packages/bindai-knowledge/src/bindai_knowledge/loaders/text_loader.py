from pathlib import Path

from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentLoader


class TextLoader(DocumentLoader):
    def __init__(
        self,
        path: str,
    ):

        self.path = Path(path)

    def load(
        self,
    ) -> list[KnowledgeDocument]:

        return [
            KnowledgeDocument(
                id=self.path.stem,
                title=self.path.name,
                content=self.path.read_text(
                    encoding="utf-8",
                ),
                metadata={
                    "path": str(self.path),
                    "extension": self.path.suffix,
                },
            )
        ]
