from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from ..node import WorkflowNode


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
        context,
    ):
        ...

    def before_execute(
        self,
        context,
    ):
        """
        Optional preprocessing.
        """
        return context

    def after_execute(
        self,
        context,
        result,
    ):
        """
        Optional postprocessing.
        """
        return context

    def execute(
        self,
        context,
    ):

        context = self.before_execute(
            context,
        )

        executable = self.get_executable(
            context,
        )

        if executable is None:
            raise RuntimeError(
                f"{self.__class__.__name__} "
                "returned no executable."
            )

        result = executable.execute(
            context,
        )

        context = self.after_execute(
            context,
            result,
        )

        return context