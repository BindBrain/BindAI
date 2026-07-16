from __future__ import annotations

from bindai_core.context import ExecutionContext


class ExecutionPipeline:

    def __init__(self):

        self._middleware = []

    def use(
        self,
        middleware,
    ):

        self._middleware.append(
            middleware,
        )

        return self

    def execute(
        self,
        agent,
        context: ExecutionContext,
    ):

        for middleware in self._middleware:

            middleware.before_execute(
                agent,
                context,
            )

        result = agent.execute(
            context,
        )

        for middleware in reversed(
            self._middleware,
        ):

            middleware.after_execute(
                agent,
                context,
                result,
            )

        return result