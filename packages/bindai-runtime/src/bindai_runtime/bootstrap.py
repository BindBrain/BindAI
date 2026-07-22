from __future__ import annotations

from .executor_registry import ExecutorRegistry


def create_registry() -> ExecutorRegistry:
    """
    Creates the runtime executor registry.

    Executors will be registered here.
    """

    return ExecutorRegistry()
