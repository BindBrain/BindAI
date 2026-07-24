from __future__ import annotations

from ..node import WorkflowNode


class ParallelNode(WorkflowNode):
    """
    Parallel node.

    The executor schedules every node in
    next_nodes automatically.
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

    def execute(
        self,
        context,
    ):
        return context