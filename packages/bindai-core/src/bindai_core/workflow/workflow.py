from __future__ import annotations

import copy
from uuid import uuid4

from .instance import WorkflowInstance
from .node import WorkflowNode


class Workflow:
    """
    Immutable workflow definition.

    A Workflow describes the execution graph but
    contains no runtime state.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self.id = str(uuid4())

        self.name = name

        self.version = 1

        #
        # Nodes indexed by id
        #

        self.nodes: dict[str, WorkflowNode] = {}

        #
        # Entry node
        #

        self.start_node: str | None = None

    #
    # Node Management
    #

    def add_node(
        self,
        node: WorkflowNode,
    ) -> WorkflowNode:
        """
        Add a node to the workflow.
        """

        if node.id in self.nodes:
            raise ValueError(f"Node '{node.id}' already exists.")

        self.nodes[node.id] = node

        if self.start_node is None:
            self.start_node = node.id

        return node

    def remove_node(
        self,
        node_id: str,
    ) -> None:
        """
        Remove a node.
        """

        if node_id not in self.nodes:
            return

        del self.nodes[node_id]

        #
        # Remove connections
        #

        for node in self.nodes.values():
            if node_id in node.next_nodes:
                node.disconnect(node_id)

        if self.start_node == node_id:
            self.start_node = next(iter(self.nodes)) if self.nodes else None

    def get(
        self,
        node_id: str,
    ) -> WorkflowNode:
        """
        Retrieve a node.
        """

        return self.nodes[node_id]

    #
    # Connections
    #

    def connect(
        self,
        source: str,
        target: str,
    ) -> None:
        """
        Connect two workflow nodes.
        """

        if source not in self.nodes:
            raise KeyError(f"Unknown source node '{source}'.")

        if target not in self.nodes:
            raise KeyError(f"Unknown target node '{target}'.")

        self.nodes[source].connect(target)

    #
    # Execution
    #

    def create_instance(
        self,
    ) -> WorkflowInstance:
        """
        Create a new execution instance.
        """

        return WorkflowInstance(self)

    #
    # Versioning
    #

    def clone(self) -> "Workflow":
        """
        Clone the workflow and increment version.
        """

        workflow = copy.deepcopy(self)

        workflow.id = str(uuid4())

        workflow.version += 1

        return workflow

    #
    # Helpers
    #

    def __contains__(
        self,
        node_id: str,
    ) -> bool:
        return node_id in self.nodes

    def __len__(
        self,
    ) -> int:
        return len(self.nodes)

    def __iter__(
        self,
    ):
        return iter(self.nodes.values())
