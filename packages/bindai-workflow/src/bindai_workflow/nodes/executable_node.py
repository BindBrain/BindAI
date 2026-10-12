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
    @abstractmethod
    def get_executable(
        self,
        context: WorkflowContext,
    ) -> Executable: ...

    def before_execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        return context

    def after_execute(
        self,
        context: WorkflowContext,
        result,
    ) -> WorkflowContext:
        return context

    def execute(
        self,
        context: WorkflowContext,
    ):
        context = self.before_execute(
            context,
        )

        executable = self.get_executable(
            context,
        )

        if executable is None:
            raise RuntimeError(f"{self.__class__.__name__} returned no executable.")

        execution_context = ExecutionContext()

        execution_context.variables = context.variables

        #
        # Propagate execution metadata from the workflow context.
        #
        # This is what allows simulation mode and future execution
        # policies to reach nested executables such as ToolNode.
        #

        execution_context.metadata.update(
            getattr(
                context,
                "metadata",
                {},
            )
        )

        result = executable.execute(
            execution_context,
        )

        context = self.after_execute(
            context,
            result,
        )

        return context
