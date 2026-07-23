from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_core.execution import (
    ExecutionRequest,
    ExecutionResponse,
)

if TYPE_CHECKING:
    from bindai_core.executable import Executable
    from bindai_core.middleware import Middleware


class ExecutionPipeline:
    """
    Coordinates the execution of an agent through middleware.
    """

    def __init__(self) -> None:
        self._middleware: list[Middleware] = []

    def use(
        self,
        middleware: Middleware,
    ) -> ExecutionPipeline:
        """
        Register middleware.
        """
        self._middleware.append(middleware)
        return self

    def execute(
        self,
        request_or_agent: ExecutionRequest | Executable,
        context: ExecutionContext | None = None,
    ) -> ExecutionResponse:

        agent: Executable

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
