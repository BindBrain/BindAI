from __future__ import annotations

from collections import defaultdict

from .edge import GraphEdge


class ExecutionGraph:
    """
    Directed execution graph.

    Supports DAG execution,
    conditional routing,
    fan-out and fan-in.
    """

    def __init__(
        self,
    ):
        self.nodes: dict = {}

        self.edges: list[GraphEdge] = []

        self._outgoing = defaultdict(
            list,
        )

        self._incoming = defaultdict(
            list,
        )

    def add_node(
        self,
        name: str,
        node,
    ):
        self.nodes[name] = node

        return self

    def add_edge(
        self,
        source: str,
        target: str,
        *,
        condition=None,
    ):
        edge = GraphEdge(
            source,
            target,
            condition,
        )

        self.edges.append(
            edge,
        )

        self._outgoing[source].append(
            edge,
        )

        self._incoming[target].append(
            edge,
        )

        return self

    #
    # Graph API
    #

    def get_node(
        self,
        name: str,
    ):
        return self.nodes[name]

    def outgoing(
        self,
        name: str,
    ):
        return self._outgoing.get(
            name,
            [],
        )

    def incoming(
        self,
        name: str,
    ):
        return self._incoming.get(
            name,
            [],
        )

    def roots(
        self,
    ):
        """
        Nodes without incoming edges.
        """

        return [
            name
            for name in self.nodes
            if len(
                self.incoming(
                    name,
                )
            )
            == 0
        ]

    def validate(
        self,
    ):

        #
        # Empty graph
        #

        if not self.nodes:
            raise ValueError(
                "Execution graph is empty."
            )

        #
        # At least one root
        #

        if not self.roots():
            raise ValueError(
                "Execution graph has no root node."
            )

        #
        # Edge validation
        #

        for edge in self.edges:

            if edge.source not in self.nodes:
                raise ValueError(
                    f"Unknown source node '{edge.source}'."
                )

            if edge.target not in self.nodes:
                raise ValueError(
                    f"Unknown target node '{edge.target}'."
                )