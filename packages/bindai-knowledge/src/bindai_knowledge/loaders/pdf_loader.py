from pathlib import Path

from pypdf import PdfReader

from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentLoader


class PDFLoader(DocumentLoader):
    def __init__(
        self,
        path: str,
    ):
        self.path = Path(path)

    def load(
        self,
    ) -> list[KnowledgeDocument]:

        reader = PdfReader(self.path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return [
            KnowledgeDocument(
                id=self.path.stem,
                title=self.path.name,
                content=text,
                metadata={
                    "path": str(self.path),
                    "extension": self.path.suffix,
                },
            )
        ]
