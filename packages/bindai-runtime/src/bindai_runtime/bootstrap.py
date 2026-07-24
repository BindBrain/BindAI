from __future__ import annotations

from bindai_task import Task
from bindai_workflow import Workflow

from .executor_registry import ExecutorRegistry
from .task_executor import TaskExecutor
from .workflow_executor import WorkflowExecutor


def create_registry() -> ExecutorRegistry:

    registry = ExecutorRegistry()

    registry.register(
        Task,
        TaskExecutor,
    )

    registry.register(
        Workflow,
        WorkflowExecutor,
    )

    return registry