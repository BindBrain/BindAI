from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bindai_core.executable import Executable

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
        runnable: Executable,
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
    ) -> Executable[Any]:

        return self.runnable
