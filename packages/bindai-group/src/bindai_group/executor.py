from __future__ import annotations

from bindai_core.context import ExecutionContext

from .result import GroupResult


class GroupExecutor:
    """
    Executes a Group using its configured process.
    """

    def execute(
        self,
        group,
        context: ExecutionContext,
    ) -> GroupResult:

        return group.process.execute(
            group,
            context,
        )