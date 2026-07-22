from __future__ import annotations


class ExecutionStep:
    """
    Base execution step.
    """

    def execute(
        self,
        agent,
        context,
    ):
        raise NotImplementedError