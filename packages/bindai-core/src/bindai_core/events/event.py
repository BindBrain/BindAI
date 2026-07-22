from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(slots=True, kw_only=True)
class Event:
    name: str

    payload: dict = field(default_factory=dict)

    id: str = field(default_factory=lambda: str(uuid4()))

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def name(self) -> str:
        raise NotImplementedError
