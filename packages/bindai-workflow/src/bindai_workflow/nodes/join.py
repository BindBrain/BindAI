from __future__ import annotations

from typing import TYPE_CHECKING

from ..node import WorkflowNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class JoinNode(WorkflowNode):
    def __init__(
        self,
        node_id: str,
        expected: int,
        name: str | None = None,
    ):
        super().__init__(
            node_id=node_id,
            name=name,
        )
        self.expected = expected

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        current = context.join_state.get(
            self.id,
            0,
        )

        current += 1

        context.join_state[self.id] = current

        if current < self.expected:
            context.waiting = True
            return context

        context.join_state.pop(
            self.id,
            None,
        )

        context.waiting = False

        return context

    def to_dict(self) -> dict:
        data = super().to_dict()

        data.update(
            {
                "expected": self.expected,
            }
        )

        return data

    def load_dict(
        self,
        data: dict,
    ) -> None:
        super().load_dict(data)

        self.expected = data["expected"]