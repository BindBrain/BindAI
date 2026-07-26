from __future__ import annotations

from bindai_core.executable import Executable

from ..node import WorkflowNode


class ExecutableNode(WorkflowNode):
    """
    Generic workflow node that wraps any Executable.
    """

    def __init__(
        self,
        node_id: str,
        executable: Executable,
        name: str | None = None,
    ):
        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.executable = executable

    def execute(
        self,
        context,
    ):
        return self.executable.execute(context)