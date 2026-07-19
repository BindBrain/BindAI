from __future__ import annotations

from ..node import WorkflowNode


class CompensationNode(
    WorkflowNode,
):
    """
    Registers a rollback action.
    """

    def __init__(
        self,
        node_id: str,
        action,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.action = action

    def execute(
        self,
        context,
    ):

        context.compensations.append(
            self.action,
        )

        return context