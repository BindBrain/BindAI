from __future__ import annotations

from .chunk import KnowledgeChunk
from .document import KnowledgeDocument


class KnowledgePipeline:
    """
    Processes loaded documents into knowledge documents.
    """

    def process(
        self,
        documents: list[KnowledgeDocument],
        chunker=None,
    ) -> list[KnowledgeDocument]:
        if chunker is None:
            return list(documents)

        processed: list[KnowledgeDocument] = []

        for document in documents:
            chunks: list[KnowledgeChunk] = chunker.chunk(document)

            for chunk in chunks:
                processed.append(
                    KnowledgeDocument(
                        id=chunk.id,
                        title=document.title,
                        content=chunk.content,
                        metadata={
                            **(document.metadata or {}),
                            **(chunk.metadata or {}),
                            "document_id": chunk.document_id,
                            "chunk": True,
                        },
                    )
                )

        return processed
