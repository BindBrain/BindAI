from bindai_core import ExecutionContext

from .executor import Executor


class BindRuntime:

    def __init__(self):

        self._executor = Executor()

    def run(self, executable):

        context = ExecutionContext()

        return self._executor.execute(
            executable,
            context,
        )