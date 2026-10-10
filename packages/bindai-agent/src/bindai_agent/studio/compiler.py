from __future__ import annotations

from bindai_agent.nodes import NodeRegistry

from .execution import StudioNodeExecutionStep
from .result import StudioExecutionResult
from .validator import validate_graph


def order_nodes(
    graph,
):

    nodes = {
        node.id: node
        for node in graph.nodes
    }

    incoming = {
        node_id: 0
        for node_id in nodes
    }

    for edge in graph.edges:

        incoming[edge.target] += 1

    queue = [
        node_id
        for node_id, count in incoming.items()
        if count == 0
    ]

    ordered = []

    while queue:

        current = queue.pop(0)

        ordered.append(
            nodes[current]
        )

        for edge in graph.edges:

            if edge.source == current:

                incoming[edge.target] -= 1

                if incoming[edge.target] == 0:

                    queue.append(
                        edge.target
                    )

    if len(ordered) != len(nodes):

        raise ValueError(
            "Graph contains a cycle"
        )

    return ordered


def compile_graph(
    graph,
):

    errors = validate_graph(
        graph
    )

    if errors:

        raise ValueError(
            errors
        )

    result = StudioExecutionResult()

    steps = []

    for node in order_nodes(graph):

        runtime_node = NodeRegistry.create(
            node.type
        )

        steps.append(
            StudioNodeExecutionStep(
                runtime_node,
                node.id,
                node.config,
                graph,
                result,
            )
        )

    return steps
