from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class KnowledgeChunk:
    """
    One chunk of a knowledge document.
    """

    id: str

    document_id: str

    content: str

    metadata: dict[str, Any] | None = None