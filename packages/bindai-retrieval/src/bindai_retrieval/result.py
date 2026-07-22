from dataclasses import dataclass

from bindai_knowledge import KnowledgeDocument


@dataclass(slots=True)
class RetrievalResult:
    """
    Documents returned from retrieval.
    """

    success: bool

    documents: list[KnowledgeDocument]

    error: str | None = None
