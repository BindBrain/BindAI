from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from ..expression import WorkflowExpression
from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class ConditionNode(WorkflowNode):
    def __init__(
        self,
        node_id: str,
        predicate: Callable[[WorkflowContext], bool] | None = None,
        expression: str | None = None,
    ):
        super().__init__(node_id)

        if predicate is None and expression is None:
            raise ValueError("ConditionNode requires either a predicate or expression.")

        if predicate is not None and expression is not None:
            raise ValueError("ConditionNode cannot use both a predicate and expression.")

        self.predicate = predicate
        self.expression = expression
        self.engine = WorkflowExpression()

        self.true_node: str | None = None
        self.false_node: str | None = None

    def when_true(self, node: WorkflowNode) -> ConditionNode:
        self.true_node = node.id
        return self

    def when_false(self, node: WorkflowNode) -> ConditionNode:
        self.false_node = node.id
        return self

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        if self.expression is not None:
            result = self.engine.evaluate(
                self.expression,
                context.variables.as_dict(),
            )
        else:
            if self.predicate is None:
                raise RuntimeError(
                    "ConditionNode requires a predicate when no expression is configured."
                )
            result = self.predicate(context)

        if result:
            if self.true_node is not None:
                context.execution_queue.append(self.true_node)
        else:
            if self.false_node is not None:
                context.execution_queue.append(self.false_node)

        return context
