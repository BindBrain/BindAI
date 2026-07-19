from __future__ import annotations

from ..node import WorkflowNode


class JoinNode(
    WorkflowNode,
):
    """
    Waits until all branches complete.
    """

    def execute(
        self,
        context,
    ):

        context.parallel_nodes.clear()

        return context