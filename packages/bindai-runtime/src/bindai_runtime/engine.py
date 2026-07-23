from __future__ import annotations

from typing import Protocol, cast

from bindai_core.context import ExecutionContext

from .executor_registry import ExecutorRegistry


class RuntimeExecutor(Protocol):
    def execute(
        self,
        context,
    ) -> None: ...


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

        cast(
            RuntimeExecutor,
            executor,
        ).execute(
            context,
        )