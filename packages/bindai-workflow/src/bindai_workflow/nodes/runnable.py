from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.runnable import Runnable

from .executable_node import ExecutableNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class RunnableNode(
    ExecutableNode,
):
    """
    Executes any BindAI Runnable.
    """

    def __init__(
        self,
        node_id: str,
        runnable: Runnable,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.runnable = runnable

    def get_executable(
        self,
        context: WorkflowContext,
    ) -> Runnable:

        return self.runnable
