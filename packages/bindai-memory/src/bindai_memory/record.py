from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class MemoryType(Enum):
    """
    Type/category of stored memory.
    """

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    WORKING = "working"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"

    def __str__(
        self,
    ) -> str:

        return self.value


@dataclass(slots=True)
class MemoryRecord:
    """
    A single memory entry.
    """

    key: str

    value: Any

    namespace: str = "default"

    type: MemoryType = MemoryType.LONG_TERM

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    importance: float = 0.5

    access_count: int = 0

    last_accessed: datetime | None = None

    expires_at: datetime | None = None

    embedding: list[float] | None = None

    score: float | None = None

    tags: list[str] = field(
        default_factory=list,
    )

    source: str | None = None

    relationships: dict[str, list[str]] = field(
        default_factory=dict,
    )

    #
    # Legacy API compatibility
    #

    related_keys: list[str] = field(
        default_factory=list,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    def __post_init__(
        self,
    ) -> None:

        if self.metadata is None:
            self.metadata = {}

        if self.tags is None:
            self.tags = []

        if self.relationships is None:
            self.relationships = {}

        if self.related_keys is None:
            self.related_keys = []

        #
        # Keep legacy and new APIs synchronized.
        #

        if not self.related_keys and "related" in self.relationships:
            self.related_keys = list(
                self.relationships["related"],
            )

        elif self.related_keys and "related" not in self.relationships:
            self.relationships["related"] = list(
                self.related_keys,
            )

    def touch(
        self,
    ) -> None:

        self.updated_at = datetime.now(
            UTC,
        )

    #
    # Tags
    #

    def add_tag(
        self,
        tag: str,
    ) -> None:

        if tag not in self.tags:
            self.tags.append(
                tag,
            )

    def remove_tag(
        self,
        tag: str,
    ) -> None:

        if tag in self.tags:
            self.tags.remove(
                tag,
            )

    def has_tag(
        self,
        tag: str,
    ) -> bool:

        return tag in self.tags

    #
    # Relationships
    #

    def add_relationship(
        self,
        relation: str,
        target: str,
    ) -> None:

        self.relationships.setdefault(
            relation,
            [],
        )

        if target not in self.relationships[relation]:
            self.relationships[relation].append(
                target,
            )

        if relation == "related" and target not in self.related_keys:
            self.related_keys.append(
                target,
            )

    def get_relationships(
        self,
        relation: str,
    ) -> list[str]:

        return list(
            self.relationships.get(
                relation,
                [],
            )
        )

    #
    # Legacy compatibility API
    #

    def add_relation(
        self,
        key: str,
    ) -> None:

        self.add_relationship(
            "related",
            key,
        )

    def remove_relation(
        self,
        key: str,
    ) -> None:

        if key in self.related_keys:
            self.related_keys.remove(
                key,
            )

        if "related" in self.relationships and key in self.relationships["related"]:
            self.relationships["related"].remove(
                key,
            )

    def has_relation(
        self,
        key: str,
    ) -> bool:

        return key in self.related_keys

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "key": self.key,
            "value": self.value,
            "namespace": self.namespace,
            "type": self.type.value,
            "metadata": self.metadata,
            "importance": self.importance,
            "access_count": self.access_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed": (self.last_accessed.isoformat() if self.last_accessed else None),
            "expires_at": (self.expires_at.isoformat() if self.expires_at else None),
            "embedding": self.embedding,
            "score": self.score,
            "tags": list(
                self.tags,
            ),
            "source": self.source,
            "relationships": dict(
                self.relationships,
            ),
            "related_keys": list(
                self.related_keys,
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> MemoryRecord:

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
            value=data.get(
                "value",
            ),
            namespace=data.get(
                "namespace",
                "default",
            ),
            type=record_type,
            metadata=data.get(
                "metadata",
                {},
            ),
            importance=data.get(
                "importance",
                0.5,
            ),
            access_count=data.get(
                "access_count",
                0,
            ),
            created_at=(
                datetime.fromisoformat(
                    data["created_at"],
                )
                if data.get(
                    "created_at",
                )
                else datetime.now(
                    UTC,
                )
            ),
            updated_at=(
                datetime.fromisoformat(
                    data["updated_at"],
                )
                if data.get(
                    "updated_at",
                )
                else datetime.now(
                    UTC,
                )
            ),
            last_accessed=(
                datetime.fromisoformat(
                    data["last_accessed"],
                )
                if data.get(
                    "last_accessed",
                )
                else None
            ),
            expires_at=(
                datetime.fromisoformat(
                    data["expires_at"],
                )
                if data.get(
                    "expires_at",
                )
                else None
            ),
            embedding=data.get(
                "embedding",
            ),
            score=data.get(
                "score",
            ),
            tags=list(
                data.get(
                    "tags",
                    [],
                )
            ),
            source=data.get(
                "source",
            ),
            relationships=dict(
                data.get(
                    "relationships",
                    {},
                )
            ),
            related_keys=list(
                data.get(
                    "related_keys",
                    data.get(
                        "relationships",
                        {},
                    ).get(
                        "related",
                        [],
                    ),
                )
            ),
        )
