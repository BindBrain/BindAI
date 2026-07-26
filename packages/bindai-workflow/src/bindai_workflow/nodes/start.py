from __future__ import annotations

from typing import TYPE_CHECKING

from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class StartNode(
    WorkflowNode,
):
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:

        return context

    def to_dict(
        self,
    ) -> dict:

        return super().to_dict()

    def load_dict(
        self,
        data: dict,
    ) -> None:

        super().load_dict(
            data,
        )
