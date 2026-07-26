from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class Resource:
    """
    Base class for every BindAI resource.
    """

    name: str

    _id: str = field(default_factory=lambda: str(uuid4()), init=False)

    @property
    def id(self) -> str:
        return self._id