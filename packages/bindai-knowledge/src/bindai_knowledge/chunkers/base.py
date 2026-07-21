from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_knowledge.chunk import KnowledgeChunk
from bindai_knowledge.document import KnowledgeDocument


class DocumentChunker(ABC):
    """
    Base class for document chunkers.
    """

    @abstractmethod
    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:
        ...