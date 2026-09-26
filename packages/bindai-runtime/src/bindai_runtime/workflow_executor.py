from __future__ import annotations

from bindai_core import ExecutionContext
from bindai_workflow import Workflow


class WorkflowExecutor:
    """
    Runtime adapter for BindAI workflows.

    The workflow package owns the actual workflow execution lifecycle.
    This class only adapts the runtime ExecutionContext to the
    WorkflowInstance/WorkflowContext model used by WorkflowExecutor.
    """

    def __init__(
        self,
        executable: Workflow,
    ) -> None:
        self.workflow = executable

    def execute(
        self,
        context: ExecutionContext,
    ):
        instance = self.workflow.create_instance()

        #
        # Transfer runtime variables into the workflow context.
        #

        instance.context.variables.update(
            context.variables,
        )

        #
        # Execute through the workflow package's real executor.
        #
        # Do not implement another workflow loop here.
        #

        result = self.workflow.executor.execute(
            instance,
        )

        #
        # Transfer resulting variables back into the runtime context.
        #

        context.variables.update(
            instance.context.variables,
        )

        return result