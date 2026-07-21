from __future__ import annotations

from bindai_knowledge.chunk import KnowledgeChunk
from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentChunker


class RecursiveChunker(DocumentChunker):

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:

        pieces = self._split(
            document.content,
        )

        chunks: list[KnowledgeChunk] = []

        current = ""

        index = 0

        for piece in pieces:

            separator = "\n\n" if current else ""

            candidate = current + separator + piece

            if len(candidate) <= self.chunk_size:

                current = candidate

                continue

            if current:

                chunks.append(

                    KnowledgeChunk(

                        id=f"{document.id}:{index}",

                        document_id=document.id,

                        content=current,

                        metadata=document.metadata,

                    )

                )

                index += 1

            current = piece

        if current:

            chunks.append(

                KnowledgeChunk(

                    id=f"{document.id}:{index}",

                    document_id=document.id,

                    content=current,

                    metadata=document.metadata,

                )

            )

        return chunks

    def _split(
        self,
        text: str,
    ) -> list[str]:

        #
        # Prefer paragraphs.
        #

        paragraphs = [

            p.strip()

            for p in text.split("\n\n")

            if p.strip()

        ]

        return paragraphs