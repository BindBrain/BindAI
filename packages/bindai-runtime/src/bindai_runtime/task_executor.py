from __future__ import annotations

from bindai_task import Task


class TaskExecutor:
    """
    Executes a Task.
    """

    def __init__(
        self,
        executable: Task,
    ) -> None:
        self.task = executable

    def execute(
        self,
        context,
    ):
        return self.task.execute(
            context,
        )