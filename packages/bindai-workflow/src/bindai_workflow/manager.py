from __future__ import annotations

from .executor import WorkflowExecutor
from .instance import WorkflowInstance
from .registry import WorkflowRegistry

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workflow import Workflow

class WorkflowManager:
    """
    High level workflow API.

    Responsible for creating,
    executing,
    resuming,
    and retrieving workflows.
    """

    def __init__(
        self,
        executor: WorkflowExecutor,
    ):

        self.executor = executor

    #
    # Registry
    #

    def register(
        self,
        workflow: Workflow,
    ) -> None:

        WorkflowRegistry.register(
            workflow,
        )

    def workflow(
        self,
        name: str,
    ) -> Workflow | None:

        return WorkflowRegistry.get(
            name,
        )

    #
    # Execution
    #

    def execute(
        self,
        workflow_name: str,
    ):

        workflow = self.workflow(
            workflow_name,
        )

        if workflow is None:
            raise ValueError(
                f'Workflow "{workflow_name}" not found.'
            )

        instance = workflow.create_instance()

        return self.executor.execute(
            instance,
        )

    def resume(
        self,
        instance: WorkflowInstance,
    ):

        return self.executor.resume(
            instance,
        )
