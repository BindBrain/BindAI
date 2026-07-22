from __future__ import annotations

from bindai_core.context import ExecutionContext

from .executor_registry import ExecutorRegistry


class ExecutionEngine:
    """
    Central execution engine.

    Resolves the appropriate executor
    for every executable.
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

        executor = self._registry.resolve(
            executable,
        )

        return executor.execute(
            executable,
            context,
        )