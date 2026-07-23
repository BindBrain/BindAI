from __future__ import annotations

from abc import ABC, abstractmethod


class ResourceContract(ABC):
    """
    Base contract implemented by every BindAI resource.
    """

    name: str

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier."""
        ...