from __future__ import annotations


class ExecutionPipeline:
    """
    Executes a sequence of steps.
    """

    def __init__(
        self,
        *steps,
    ):
        self.steps = list(
            steps,
        )

    def add(
        self,
        step,
    ):

        self.steps.append(
            step,
        )

    def execute(
        self,
        agent,
        context,
    ):

        for step in self.steps:

            result = step.execute(
                agent,
                context,
            )

            if result is not None:

                return result

        return None