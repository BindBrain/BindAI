from __future__ import annotations

from bindai_workflow import Workflow


class WorkflowExecutor:
    """
    Executes a Workflow sequentially.
    """

    def __init__(
        self,
        executable: Workflow,
    ) -> None:
        self.workflow = executable

    def execute(
        self,
        context,
    ):
        node_id = self.workflow.start_node

        while node_id is not None:
            node = self.workflow.get(
                node_id,
            )

            node.execute(
                context,
            )

            node_id = node.next_node

        return context
