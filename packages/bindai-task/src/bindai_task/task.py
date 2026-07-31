from __future__ import annotations

from bindai_agent import Agent
from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable

from .result import TaskResult
from .state import TaskState


class Task(Executable):
    """
    Represents one unit of work.
    """

    def __init__(
        self,
        *,
        description: str,
        agent: Agent,
        expected_output: str | None = None,
    ):

        self.description = description

        self.agent = agent

        self.expected_output = expected_output

        self.state = TaskState.PENDING

        self.result: TaskResult | None = None

    def execute(
        self,
        context: ExecutionContext,
    ) -> TaskResult:

        self.state = TaskState.RUNNING

        try:
            response = self.agent.chat(
                self.description,
            )

            output = response.output if hasattr(response, "output") else response

            self.result = TaskResult(
                success=True,
                output=output,
            )

            self.state = TaskState.COMPLETED

            return self.result

        except Exception as ex:
            self.result = TaskResult(
                success=False,
                error=str(ex),
            )

            self.state = TaskState.FAILED

            return self.result
