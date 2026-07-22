from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class GraphNode(ABC):
    """
    Base executable graph node.

    Every node receives the shared
    execution context and may mutate it.
    """

    def __init__(
        self,
        name: str | None = None,
    ):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def execute(
        self,
        agent,
        context,
    ):
        """
        Execute the node.
        """
        ...

    #
    # Optional lifecycle hooks
    #

    def before_execute(
        self,
        agent,
        context,
    ):
        pass

    def after_execute(
        self,
        agent,
        context,
    ):
        pass

    def run(
        self,
        agent,
        context,
    ):
        self.before_execute(
            agent,
            context,
        )

        result = self.execute(
            agent,
            context,
        )

        self.after_execute(
            agent,
            context,
        )

        return result
