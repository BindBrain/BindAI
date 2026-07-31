from __future__ import annotations


class ExecutionPipeline:
    """
    Executes the agent pipeline.

    The pipeline automatically loops while the
    model requests tool execution.
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

        #
        # Initialization / memory / knowledge
        #

        initialization = self.steps[:-3]

        #
        # Model
        #

        model_step = self.steps[-3]

        #
        # Tool execution
        #

        tool_step = self.steps[-2]

        #
        # Finish
        #

        finish_step = self.steps[-1]

        #
        # Run initialization once.
        #

        for step in initialization:
            result = step.execute(
                agent,
                context,
            )

            if result is not None:
                return result

        state = context.data

        while True:
            #
            # Ask model.
            #

            model_step.execute(
                agent,
                context,
            )

            state = context.data

            #
            # No tools requested.
            #

            if state.response is None or not state.response.tool_calls:
                return finish_step.execute(
                    agent,
                    context,
                )

            #
            # Prevent infinite loops.
            #

            state.iterations += 1

            if state.iterations >= agent.configuration.max_tool_iterations:
                return finish_step.execute(
                    agent,
                    context,
                )

            #
            # Execute requested tools.
            #

            tool_step.execute(
                agent,
                context,
            )
