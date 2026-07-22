from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable, ExecutionResult
from bindai_core.runtime import BindRuntime


class FakeExecutable(Executable):
    def execute(
        self,
        context,
    ):

        return ExecutionResult(
            success=True,
        )


def test_runtime_execute():

    runtime = BindRuntime()

    result = runtime.execute(
        FakeExecutable(),
        ExecutionContext(),
    )

    assert result.success
