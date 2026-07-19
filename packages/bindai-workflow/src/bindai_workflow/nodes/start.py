from __future__ import annotations

from ..node import WorkflowNode


class StartNode(
    WorkflowNode,
):

    def execute(
        self,
        context,
    ):

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