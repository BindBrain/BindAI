from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable

from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class ExecutableNode(
    WorkflowNode,
    ABC,
):
    """
    Base class for workflow nodes that execute another object.
    """

    @abstractmethod
    def get_executable(
        self,
        context: WorkflowContext,
    ) -> Executable: ...

    def before_execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        """
        Optional preprocessing.
        """
        return context

    def after_execute(
        self,
        context: WorkflowContext,
        result,
    ) -> WorkflowContext:
        """
        Optional postprocessing.
        """
        return context

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:

        context = self.before_execute(
            context,
        )

        executable = self.get_executable(
            context,
        )

        if executable is None:
            raise RuntimeError(f"{self.__class__.__name__} returned no executable.")

        #
        # WorkflowContext -> ExecutionContext adapter
        #

        execution_context = ExecutionContext()

        execution_context.variables = context.variables

        result = executable.execute(
            execution_context,
        )

        context = self.after_execute(
            context,
            result,
        )

        return context
