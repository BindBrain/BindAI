from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class KnowledgeDocument:
    """
    Represents one knowledge document.
    """

    id: str

    title: str

    content: str

    metadata: dict[str, Any] | None = None