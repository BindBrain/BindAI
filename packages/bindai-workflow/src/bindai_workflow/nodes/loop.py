from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from ..expression import WorkflowExpression
from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class LoopNode(WorkflowNode):
    """
    Repeats execution while predicate returns True.

    Serialized workflows may use an expression instead of a Python
    callable predicate.

    next_nodes[0] = loop body
    next_nodes[1] = exit node
    """

    def __init__(
        self,
        node_id: str,
        predicate: Callable[[WorkflowContext], bool] | None = None,
        expression: str | None = None,
        name: str | None = None,
    ):
        super().__init__(
            node_id=node_id,
            name=name,
        )

        if predicate is None and expression is None:
            raise ValueError("LoopNode requires either a predicate or expression.")

        if predicate is not None and expression is not None:
            raise ValueError("LoopNode cannot use both a predicate and expression.")

        self.predicate = predicate
        self.expression = expression
        self.engine = WorkflowExpression()

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()

        if self.expression is not None:
            data["expression"] = self.expression

        return data

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        if len(self.next_nodes) < 2:
            raise RuntimeError("LoopNode requires two next nodes (body and exit).")

        if self.expression is not None:
            result = self.engine.evaluate(
                self.expression,
                context.variables.as_dict(),
            )
        else:
            if self.predicate is None:
                raise RuntimeError(
                    "LoopNode requires a predicate when no expression is configured."
                )

            result = self.predicate(context)

        if result:
            context.current_node = self.next_nodes[0]
        else:
            context.current_node = self.next_nodes[1]

        return context
