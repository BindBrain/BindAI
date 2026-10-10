from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StudioNode:
    id: str
    type: str
    config: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class StudioEdge:
    source: str
    source_port: str
    target: str
    target_port: str

    mapping: str | None = None


@dataclass
class StudioGraph:

    nodes: list[StudioNode] = field(
        default_factory=list
    )

    edges: list[StudioEdge] = field(
        default_factory=list
    )


    def add_node(
        self,
        node: StudioNode,
    ):
        self.nodes.append(
            node
        )


    def connect(
        self,
        edge: StudioEdge,
    ):
        self.edges.append(
            edge
        )
