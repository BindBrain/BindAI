from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from .result import ExecutionResult
from .state import ExecutionState
from .step import ExecutionStep

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext

    from bindai_agent.agent import Agent


class ExecutionPipeline:
    """
    Executes the agent execution pipeline.

    Initialization steps execute once.

    The model/tool loop repeats until
    no tool calls remain or the maximum
    iteration count is reached.
    """

    def __init__(
        self,
        steps: Sequence[ExecutionStep] | None = None,
    ) -> None:
        self.steps: list[ExecutionStep] = list(steps or [])

    def add(
        self,
        step: ExecutionStep,
    ) -> None:
        self.steps.append(step)

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ExecutionResult:
        if len(self.steps) < 3:
            raise RuntimeError("ExecutionPipeline requires at least model, tool and finish steps.")

        initialization = self.steps[:-3]

        model_step = self.steps[-3]
        tool_step = self.steps[-2]
        finish_step = self.steps[-1]

        for step in initialization:
            result = step.execute(
                agent,
                context,
            )

            if result is not None:
                return result

        while True:
            model_step.execute(
                agent,
                context,
            )

            state = cast(
                ExecutionState,
                context.data,
            )

            if state.response is None or not state.response.tool_calls:
                return finish_step.execute(
                    agent,
                    context,
                )

            if state.iterations >= agent.configuration.max_tool_iterations:
                return finish_step.execute(
                    agent,
                    context,
                )

            tool_step.execute(
                agent,
                context,
            )
