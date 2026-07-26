from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_workflow.node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext

class ConditionNode(WorkflowNode):

    def __init__(
        self,
        node_id: str,
        predicate: Callable[[WorkflowContext], bool],
    ):
        super().__init__(node_id)

        self.predicate = predicate

        self.true_node: str | None = None
        self.false_node: str | None = None

    def when_true(
        self,
        node: WorkflowNode,
    ):
        self.true_node = node.id
        return self

    def when_false(
        self,
        node: WorkflowNode,
    ):
        self.false_node = node.id
        return self

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
    
        if self.predicate(context):
            if self.true_node:
                context.execution_queue.append(
                    self.true_node,
                )
        else:
            if self.false_node:
                context.execution_queue.append(
                    self.false_node,
                )

        return context