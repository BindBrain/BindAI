from __future__ import annotations

from bindai_knowledge.chunk import KnowledgeChunk
from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentChunker


class FixedChunker(DocumentChunker):
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

        chunks: list[KnowledgeChunk] = []

        start = 0

        index = 0

        while start < len(document.content):
            end = start + self.chunk_size

            text = document.content[start:end]

            chunks.append(
                KnowledgeChunk(
                    id=f"{document.id}:{index}",
                    document_id=document.id,
                    content=text,
                    metadata=document.metadata,
                )
            )

            start += self.chunk_size - self.overlap

            index += 1

        return chunks
