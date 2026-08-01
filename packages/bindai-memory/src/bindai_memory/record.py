from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from datetime import datetime, timezone


class MemoryType(Enum):
    """
    Type/category of stored memory.
    """

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    WORKING = "working"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"

    def __str__(self) -> str:
        return self.value


@dataclass(slots=True)
class MemoryRecord:
    """
    A single memory entry.

    Represents data stored by memory providers.
    """

    key: str

    value: Any

    namespace: str = "default"

    type: MemoryType = MemoryType.LONG_TERM

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    #
    # Semantic search
    #

    embedding: list[float] | None = None

    score: float | None = None

    #
    # Lifecycle tracking
    #

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    def __post_init__(self) -> None:
        """
        Normalize record values after creation.
        """

        if self.metadata is None:
            self.metadata = {}

    def touch(self) -> None:
        """
        Update modification timestamp.
        """

        self.updated_at = datetime.now(
            timezone.utc,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert record into a serializable dictionary.
        """

        return {
            "key": self.key,
            "value": self.value,
            "namespace": self.namespace,
            "type": self.type.value,
            "metadata": self.metadata,
            "embedding": self.embedding,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> MemoryRecord:
        """
        Create a MemoryRecord from a dictionary.
        """

        memory_type = data.get(
            "type",
            MemoryType.LONG_TERM.value,
        )

        if isinstance(
            memory_type,
            MemoryType,
        ):
            record_type = memory_type
        else:
            record_type = MemoryType(
                memory_type,
            )

        return cls(
            key=data["key"],
            value=data.get("value"),
            namespace=data.get(
                "namespace",
                "default",
            ),
            type=record_type,
            metadata=data.get(
                "metadata",
                {},
            ),
            embedding=data.get(
                "embedding",
            ),
            score=data.get(
                "score",
            ),
            created_at=(
                datetime.fromisoformat(
                    data["created_at"]
                )
                if data.get("created_at")
                else datetime.now(timezone.utc)
            ),
            updated_at=(
                datetime.fromisoformat(
                    data["updated_at"]
                )
                if data.get("updated_at")
                else datetime.now(timezone.utc)
            ),
        )