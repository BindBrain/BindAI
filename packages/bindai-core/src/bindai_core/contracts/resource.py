from __future__ import annotations

from abc import ABC, abstractmethod


class ResourceContract(ABC):
    """
    Base contract implemented by every BindAI resource.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name."""
        raise NotImplementedError