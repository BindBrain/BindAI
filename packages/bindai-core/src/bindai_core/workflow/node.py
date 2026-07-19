from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class WorkflowNode(ABC):
    """
    Base class for every workflow node.

    Every executable node inside a workflow derives
    from this class.
    """

    def __init__(
        self,
        node_id: str,
        name: str | None = None,
    ) -> None:

        self.id = node_id
        self.name = name or node_id

        #
        # Outgoing connections
        #

        self.next_nodes: list[str] = []

        #
        # Optional metadata
        #

        self.metadata: dict[str, Any] = {}

    def connect(
        self,
        node_id: str,
    ) -> None:
        """
        Connect this node to another node.
        """

        if node_id not in self.next_nodes:
            self.next_nodes.append(node_id)

    def disconnect(
        self,
        node_id: str,
    ) -> None:
        """
        Remove an outgoing connection.
        """

        if node_id in self.next_nodes:
            self.next_nodes.remove(node_id)

    @abstractmethod
    def execute(
        self,
        context,
    ) -> None:
        """
        Execute this node.

        Implementations should modify the workflow
        context and return nothing.
        """
        ...

    def to_dict(self) -> dict:
        """
        Serialize this node.
        """

        return {
            "id": self.id,
            "name": self.name,
            "next_nodes": list(self.next_nodes),
            "metadata": dict(self.metadata),
        }

    def load_dict(
        self,
        data: dict,
    ) -> None:
        """
        Restore node state.
        """

        self.id = data["id"]
        self.name = data.get("name", self.id)
        self.next_nodes = list(
            data.get("next_nodes", [])
        )
        self.metadata = dict(
            data.get("metadata", {})
        )