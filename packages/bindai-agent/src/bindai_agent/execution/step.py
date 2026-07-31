from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext

    from bindai_agent.agent import Agent


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
