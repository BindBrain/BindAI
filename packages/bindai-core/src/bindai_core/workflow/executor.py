from bindai_core.context import ExecutionContext

from .result import WorkflowResult


class WorkflowExecutor:

    def execute(
        self,
        workflow,
        context: ExecutionContext,
    ):

        try:

            for node in workflow.nodes:

                executable = node.executable

                executable.execute(context)

            return WorkflowResult(
                success=True,
            )

        except Exception as ex:

            return WorkflowResult(
                success=False,
                error=str(ex),
            )