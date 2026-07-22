from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from bindai_agent.agent import Agent
    from bindai_core.context import ExecutionContext


class ExecutionStep(ABC):
    """
    Base class for every execution pipeline step.
    """

    @abstractmethod
    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> Any:
        """
        Execute the step.

        Return None to continue the pipeline.

        Return any value to terminate the pipeline
        and return that value.
        """
        ...