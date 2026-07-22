from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Process(ABC):
    """
    Base execution strategy.
    """

    @abstractmethod
    def execute(
        self,
        group,
    ): ...
