from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SearchType = Literal[
    "keyword",
    "vector",
    "hybrid",
]


@dataclass(slots=True)
class KnowledgeSearchOptions:
    """
    Options controlling document search.
    """

    limit: int = 5

    filters: dict[str, object] | None = None

    min_score: float = 0.0

    search_type: SearchType = "keyword"
