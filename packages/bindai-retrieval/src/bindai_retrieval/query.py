from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RetrievalQuery:
    """
    Retrieval request.
    """

    text: str

    namespace: str = "default"

    limit: int = 10

    metadata: dict[str, Any] | None = None