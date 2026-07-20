from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_knowledge.document import KnowledgeDocument


class DocumentLoader(ABC):

    @abstractmethod
    def load(
        self,
    ) -> list[KnowledgeDocument]:
        ...