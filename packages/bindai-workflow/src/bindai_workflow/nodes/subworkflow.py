from __future__ import annotations

from ..node import WorkflowNode


class SubWorkflowNode(
    WorkflowNode,
):
    """
    Executes another workflow.
    """

    def __init__(
        self,
        node_id: str,
        workflow_id: str,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.workflow_id = workflow_id

    def execute(
        self,
        context,
    ):

        context.subworkflow = self.workflow_id

        return context

    def to_dict(
        self,
    ) -> dict:

        data = super().to_dict()

        data.update(
            {
                "workflow_id": self.workflow_id,
            }
        )

        return data

    def load_dict(
        self,
        data: dict,
    ) -> None:

        super().load_dict(
            data,
        )

        self.workflow_id = data["workflow_id"]
