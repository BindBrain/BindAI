from __future__ import annotations

from .edge import GraphEdge


class ExecutionGraph:

    def __init__(self):

        self.nodes = {}

        self.edges = []

    def add_node(
        self,
        name,
        node,
    ):

        self.nodes[name] = node

        return self

    def add_edge(
        self,
        source,
        target,
        *,
        condition=None,
    ):

        self.edges.append(

            GraphEdge(
                source,
                target,
                condition,
            )

        )

        return self