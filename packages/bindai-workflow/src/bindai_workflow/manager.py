from __future__ import annotations

from .executor import WorkflowExecutor
from .instance import WorkflowInstance
from .registry import WorkflowRegistry


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
        registry: WorkflowRegistry,
        executor: WorkflowExecutor,
    ):

        self.registry = registry

        self.executor = executor

    #
    # Registry
    #

    def register(
        self,
        workflow,
    ):

        self.registry.register(
            workflow,
        )

    def workflow(
        self,
        name: str,
    ):

        return self.registry.get(
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