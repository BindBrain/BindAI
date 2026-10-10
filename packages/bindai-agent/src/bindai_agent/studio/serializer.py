from __future__ import annotations

from .graph import (
    StudioGraph,
    StudioNode,
    StudioEdge,
)


def graph_to_dict(
    graph: StudioGraph,
):

    return {
        "nodes": [
            {
                "id": node.id,
                "type": node.type,
                "config": node.config,
            }
            for node in graph.nodes
        ],
        "edges": [
            {
                "source": edge.source,
                "source_port": edge.source_port,
                "target": edge.target,
                "target_port": edge.target_port,
                "mapping": edge.mapping,
            }
            for edge in graph.edges
        ],
    }


def graph_from_dict(
    data: dict,
):

    graph = StudioGraph()

    for node in data.get(
        "nodes",
        [],
    ):

        graph.add_node(
            StudioNode(
                id=node["id"],
                type=node["type"],
                config=node.get(
                    "config",
                    {},
                ),
            )
        )


    for edge in data.get(
        "edges",
        [],
    ):

        graph.connect(
            StudioEdge(
                source=edge["source"],
                source_port=edge["source_port"],
                target=edge["target"],
                target_port=edge["target_port"],
                mapping=edge.get(
                    "mapping"
                ),
            )
        )

    return graph
