from __future__ import annotations

from .node import WorkflowNode
from .edge import WorkflowEdge


class Workflow:

    def __init__(
        self,
        name: str,
    ):

        self.name = name

        self.nodes: list[WorkflowNode] = []

        self.edges: list[WorkflowEdge] = []

    def add_node(
        self,
        node: WorkflowNode,
    ):

        self.nodes.append(node)

        return self

    def connect(
        self,
        source: str,
        target: str,
    ):

        self.edges.append(
            WorkflowEdge(
                source,
                target,
            )
        )

        return self