from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable, ExecutionResult

from .options import RuntimeOptions
from .state import RuntimeState


class BindRuntime:
    """
    Executes any BindAI Executable.
    """

    def __init__(
        self,
        options: RuntimeOptions | None = None,
    ):
        self.options = options or RuntimeOptions()
        self.state = RuntimeState.CREATED

    def execute(
        self,
        executable: Executable,
        context: ExecutionContext | None = None,
    ) -> ExecutionResult:

        if context is None:
            context = ExecutionContext()

        self.state = RuntimeState.RUNNING

        result: ExecutionResult = executable.execute(context)

        self.state = RuntimeState.STOPPED

        return result
