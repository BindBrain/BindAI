from __future__ import annotations

from collections import deque


class GraphExecutor:
    """
    Executes an ExecutionGraph.

    Supports:
        • DAG traversal
        • conditional routing
        • multiple outgoing edges
        • future parallel execution
    """

    def execute(
        self,
        graph,
        agent,
        context,
    ):
        queue = deque(
            graph.roots(),
        )

        visited = set()

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(
                current,
            )

            node = graph.get_node(
                current,
            )

            node.run(
                agent,
                context,
            )

            for edge in graph.outgoing(
                current,
            ):
                #
                # Conditional edge
                #

                if edge.condition is not None:
                    if not edge.condition(
                        context,
                    ):
                        continue

                queue.append(
                    edge.target,
                )
