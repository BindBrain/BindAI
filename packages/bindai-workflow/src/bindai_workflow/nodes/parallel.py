from __future__ import annotations

from ..node import WorkflowNode


class ParallelNode(
    WorkflowNode,
):
    """
    Starts multiple execution branches.
    """

    def __init__(
        self,
        node_id: str,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.branches: list[str] = []

    def execute(
        self,
        context,
    ):

        #
        # Queue every branch.
        #

        context.parallel_nodes.extend(
            self.branches,
        )

        #
        # Execute first branch immediately.
        #

        if self.branches:
            context.current_node = self.branches[0]

        return context
