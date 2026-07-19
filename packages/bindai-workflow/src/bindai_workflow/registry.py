from __future__ import annotations

from .workflow import Workflow


class WorkflowRegistry:
    """
    Stores workflows by ID.
    """

    def __init__(self):

        self._workflows = {}

    def register(
        self,
        workflow: Workflow,
    ):

        self._workflows[
            workflow.id
        ] = workflow

    def get(
        self,
        workflow_id: str,
    ) -> Workflow | None:

        return self._workflows.get(
            workflow_id,
        )

    def all(
        self,
    ) -> list[Workflow]:

        return list(
            self._workflows.values()
        )

    def remove(
        self,
        workflow_id: str,
    ):

        self._workflows.pop(
            workflow_id,
            None,
        )