from __future__ import annotations

from typing import TYPE_CHECKING

from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


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
        context: WorkflowContext,
    ) -> WorkflowContext:
        return context