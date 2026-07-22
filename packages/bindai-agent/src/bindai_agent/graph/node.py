from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class GraphNode(ABC):

    @abstractmethod
    def execute(
        self,
        agent,
        context,
    ):
        ...