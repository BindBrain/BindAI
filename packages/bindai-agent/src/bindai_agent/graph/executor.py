from __future__ import annotations


class GraphExecutor:

    def execute(
        self,
        graph,
        agent,
        context,
    ):

        current = "start"

        while current:

            node = graph.nodes[current]

            node.execute(
                agent,
                context,
            )

            next_node = None

            for edge in graph.edges:

                if edge.source == current:

                    next_node = edge.target

                    break

            current = next_node