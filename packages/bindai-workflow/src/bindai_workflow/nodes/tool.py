from __future__ import annotations

from ..node import WorkflowNode


class ToolNode(
    WorkflowNode,
):

    def __init__(
        self,
        node_id: str,
        tool: str,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.tool = tool

    def execute(
        self,
        context,
    ):

        #
        # Existing execution logic
        #

        return context

    def to_dict(
        self,
    ):

        data = super().to_dict()

        data["tool"] = self.tool

        return data

    def load_dict(
        self,
        data: dict,
    ):

        super().load_dict(
            data,
        )

        self.tool = data["tool"]