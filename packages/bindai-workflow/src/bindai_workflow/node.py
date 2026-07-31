from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import WorkflowContext
from typing import cast
from .context import WorkflowContext

class WorkflowNode(ABC):
    """
    Base workflow node.
    """

    def __init__(
        self,
        node_id: str,
        name: str | None = None,
    ):

        self.id = node_id

        self.name = name or node_id

        self.next_nodes: list[str] = []

    @abstractmethod
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext: ...

    #
    # Serialization
    #

    def to_dict(
        self,
    ) -> dict[str, object]:

        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "next_nodes": list(
                self.next_nodes,
            ),
        }

    def load_dict(
        self,
        data: dict[str, object],
    ) -> None:

        self.next_nodes = cast(
            list[str],
            data.get(
                "next_nodes",
                [],
            ),
        )

    @property
    def next_node(
        self,
    ) -> str | None:

        if not self.next_nodes:
            return None

        return self.next_nodes[0]
