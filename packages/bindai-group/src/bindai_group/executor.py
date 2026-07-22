from __future__ import annotations

from .result import GroupResult


class GroupExecutor:
    """
    Executes a Group using its configured process.
    """

    def execute(
        self,
        group,
    ) -> GroupResult:

        return group.process.execute(
            group,
        )
