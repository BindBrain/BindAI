from __future__ import annotations

from abc import ABC
from abc import abstractmethod


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
        context,
    ):
        ...

    #
    # Serialization
    #

    def to_dict(
        self,
    ) -> dict:

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
        data: dict,
    ):

        self.next_nodes = list(

            data.get(
                "next_nodes",
                [],
            )

        )

    @property
    def next_node(
        self,
    ):

        if not self.next_nodes:

            return None

        return self.next_nodes[0]