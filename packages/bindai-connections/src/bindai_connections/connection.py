from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Connection(ABC):
    """Base interface for external service connections."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the connection name."""
        ...

    @abstractmethod
    def connect(self) -> None:
        """Establish the connection."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """Return whether the connection is active."""
        ...

    @abstractmethod
    def send(self, payload: Any) -> Any:
        """Send a payload through the connection."""
        ...
