from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RetrievalQuery:
    """
    Represents one retrieval request.
    """

    query: str

    limit: int = 5

    filters: dict[str, Any] | None = None