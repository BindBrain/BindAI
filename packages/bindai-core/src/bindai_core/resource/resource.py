from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from bindai_core.contracts.resource import ResourceContract


@dataclass(slots=True)
class Resource(ResourceContract):
    """
    Base class for every BindAI resource.
    """

    name: str

    _id: str = field(default_factory=lambda: str(uuid4()), init=False)

    @property
    def id(self) -> str:
        return self._id
