from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.execution import (
    ExecutionRequest,
    ExecutionResponse,
)


class ExecutionPipeline:
    """
    Coordinates the execution of an agent through middleware.
    """

    def __init__(self):
        self._middleware = []

    def use(self, middleware):
        """
        Register middleware.
        """
        self._middleware.append(middleware)
        return self

    def execute(
        self,
        request_or_agent,
        context: ExecutionContext | None = None,
    ):

        # New API
        if isinstance(request_or_agent, ExecutionRequest):
            request = request_or_agent
            agent = request.agent
            context = request.context

        # Old API
        else:
            agent = request_or_agent

            if context is None:
                raise ValueError("ExecutionContext is required.")

        # Before execution
        for middleware in self._middleware:
            middleware.before_execute(
                agent,
                context,
            )

        # Execute agent
        result = agent.execute(
            context,
        )

        # After execution
        for middleware in reversed(self._middleware):
            middleware.after_execute(
                agent,
                context,
                result,
            )

        return ExecutionResponse(
            result=result,
        )
