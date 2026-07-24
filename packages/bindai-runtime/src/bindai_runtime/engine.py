from __future__ import annotations

from bindai_core.context import ExecutionContext

from .executor_registry import ExecutorRegistry


class ExecutionEngine:
    """
    Resolves and executes runtime executors.
    """

    def __init__(
        self,
        registry: ExecutorRegistry,
    ):
        self._registry = registry

    def execute(
        self,
        executable,
        context: ExecutionContext,
    ):

        executor_type = self._registry.resolve(
            executable,
        )

        executor = executor_type(
            executable,
        )

        return executor.execute(
            context,
        )