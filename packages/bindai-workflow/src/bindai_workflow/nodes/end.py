from __future__ import annotations

from ..node import WorkflowNode


class EndNode(
    WorkflowNode,
):

    def execute(
        self,
        context,
    ):

        context.completed = True

        return context

    def to_dict(
        self,
    ):

        return super().to_dict()

    def load_dict(
        self,
        data: dict,
    ):

        super().load_dict(
            data,
        )