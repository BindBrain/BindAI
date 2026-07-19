from __future__ import annotations

from ..expression import WorkflowExpression
from ..node import WorkflowNode


class DecisionNode(
    WorkflowNode,
):

    def __init__(
        self,
        node_id: str,
        expression: str,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.expression = expression

        self.true_node = None

        self.false_node = None

        self.engine = WorkflowExpression()

    def execute(
        self,
        context,
    ):

        result = self.engine.evaluate(

            self.expression,

            context.variables,

        )

        context.current_node = (

            self.true_node

            if result

            else self.false_node

        )

        return context

    def to_dict(
        self,
    ):

        data = super().to_dict()

        data.update(

            {

                "expression": self.expression,

                "true_node": self.true_node,

                "false_node": self.false_node,

            }

        )

        return data

    def load_dict(
        self,
        data: dict,
    ):

        super().load_dict(
            data,
        )

        self.expression = data["expression"]

        self.true_node = data.get(
            "true_node",
        )

        self.false_node = data.get(
            "false_node",
        )