from __future__ import annotations

from .executor import Executor


class ExecutorRegistry:
    def __init__(self):
        self._executors: dict[type, type[Executor]] = {}

    def register(
        self,
        executable_type: type,
        executor: type[Executor],
    ) -> None:

        self._executors[executable_type] = executor

    def resolve(
        self,
        executable,
    ) -> type[Executor]:

        for executable_type, executor in self._executors.items():
            if isinstance(executable, executable_type):
                return executor

        raise RuntimeError(f"No executor registered for {type(executable).__name__}.")
