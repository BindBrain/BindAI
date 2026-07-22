from bindai_core import ExecutionContext
from bindai_core import ExecutionState

from .result import ExecutionResult


class Executor:
    def execute(
        self,
        executable,
        context: ExecutionContext,
    ) -> ExecutionResult:

        try:
            context.state = ExecutionState.RUNNING

            value = executable.execute(context)

            context.state = ExecutionState.COMPLETED

            return ExecutionResult(
                success=True,
                value=value,
            )

        except Exception as ex:
            context.state = ExecutionState.FAILED

            return ExecutionResult(
                success=False,
                error=ex,
            )
