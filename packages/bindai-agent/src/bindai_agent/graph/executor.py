from __future__ import annotations

from collections import deque


class GraphExecutor:
    """
    Executes an execution graph.

    Supports:

    - DAG execution
    - conditional routing
    - multiple outgoing edges
    - join-safe traversal
    """

    def execute(
        self,
        graph,
        agent,
        context,
    ):

        graph.validate()
        
        queue = deque(graph.roots())

        completed = set()

        while queue:

            node_id = queue.popleft()

            #
            # Already executed
            #

            if node_id in completed:
                continue

            node = graph.get_node(
                node_id,
            )

            #
            # Execute node
            #

            node.run(
                agent,
                context,
            )

            completed.add(
                node_id,
            )

            #
            # Route outgoing edges
            #

            for edge in graph.outgoing(
                node_id,
            ):

                #
                # Conditional edge
                #

                if edge.condition is not None:

                    if not edge.condition(
                        context,
                    ):
                        continue

                #
                # Queue next node
                #

                queue.append(
                    edge.target,
                )

        return context