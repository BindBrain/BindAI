from __future__ import annotations


class ExecutionPipeline:
    """
    Executes execution steps sequentially.
    """

    def __init__(
        self,
        steps=None,
    ):
        self.steps = list(steps or [])

    def add(
        self,
        step,
    ):
        self.steps.append(step)

    def execute(
        self,
        agent,
        context,
    ):

        while True:

            for step in self.steps:

                result = step.execute(
                    agent,
                    context,
                )

                if result is not None:
                    return result