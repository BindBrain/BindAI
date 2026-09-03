from __future__ import annotations

from bindai_knowledge.chunk import KnowledgeChunk
from bindai_knowledge.document import KnowledgeDocument

from .base import DocumentChunker


class RecursiveChunker(DocumentChunker):
    """
    Splits documents into bounded, overlapping chunks.

    The chunker prefers paragraph boundaries first, then progressively
    smaller boundaries when a piece is too large.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 0,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if overlap < 0:
            raise ValueError("overlap must not be negative")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:

        if not document.content.strip():
            return []

        pieces = self._split(document.content)

        text_chunks = self._build_chunks(pieces)

        return [
            KnowledgeChunk(
                id=f"{document.id}:{index}",
                document_id=document.id,
                content=content,
                metadata=document.metadata,
            )
            for index, content in enumerate(text_chunks)
        ]

    def _build_chunks(
        self,
        pieces: list[str],
    ) -> list[str]:

        chunks: list[str] = []

        current = ""

        for piece in pieces:
            if not piece:
                continue

            # A single paragraph is larger than the allowed chunk size.
            # Flush the current paragraph group first, then split the
            # oversized paragraph independently.
            if len(piece) > self.chunk_size:
                if current:
                    chunks.append(current)
                    current = ""

                chunks.extend(
                    self._split_large_piece(piece)
                )

                continue

            separator = "\n\n" if current else ""

            candidate = current + separator + piece

            if len(candidate) <= self.chunk_size:
                current = candidate
                continue

            # The next paragraph does not fit. Finish the current chunk.
            #
            # Important:
            # We intentionally do NOT add overlap here. Paragraph boundaries
            # are preferred over overlap.
            if current:
                chunks.append(current)

            current = piece

        if current:
            chunks.append(current)

        return chunks

    def _split_large_piece(
        self,
        text: str,
    ) -> list[str]:

        text = text.strip()

        if not text:
            return []

        chunks: list[str] = []

        start = 0

        while start < len(text):
            end = min(
                start + self.chunk_size,
                len(text),
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = end - self.overlap

        return chunks

    def _overlap_text(
        self,
        text: str,
    ) -> str:

        if not text or self.overlap == 0:
            return ""

        return text[-self.overlap :]

    def _split(
        self,
        text: str,
    ) -> list[str]:

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        return paragraphs