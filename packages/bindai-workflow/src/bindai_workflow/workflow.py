from __future__ import annotations

from .node import WorkflowNode
from .instance import WorkflowInstance

import uuid

class Workflow:
    """
    Represents an executable workflow.
    """

    def __init__(
        self,
        name: str | None = None,
    ):

        self.name = (
            name
            or self.id
        )

        self.nodes: dict[
            str,
            WorkflowNode,
        ] = {}

        self.id = str(
            uuid.uuid4(),
        )

        self.version = 1

        self.start_node: str | None = None

    def add_node(
        self,
        node: WorkflowNode,
    ):

        self.nodes[
            node.id
        ] = node

        if self.start_node is None:

            self.start_node = node.id

    def get(
        self,
        node_id: str,
    ) -> WorkflowNode:

        return self.nodes[
            node_id
        ]

    def create_instance(
        self,
    ) -> WorkflowInstance:

        return WorkflowInstance(
            self,
        )

    def clone(self):

        import copy

        workflow = copy.deepcopy(
            self,
        )

        workflow.version += 1

        return workflow