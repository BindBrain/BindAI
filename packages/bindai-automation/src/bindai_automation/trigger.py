from __future__ import annotations

from abc import ABC, abstractmethod


class Trigger(ABC):
    """
    Base abstraction for automation triggers.
    """

    def __init__(self) -> None:
        self.enabled = True

    def enable(self) -> Trigger:
        self.enabled = True
        return self

    def disable(self) -> Trigger:
        self.enabled = False
        return self

    @abstractmethod
    def attach(self) -> None:
        """
        Attach the trigger to its event source.
        """
        ...

    @abstractmethod
    def detach(self) -> None:
        """
        Detach the trigger from its event source.
        """
        ...