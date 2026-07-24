from __future__ import annotations

from ..node import WorkflowNode


class JoinNode(WorkflowNode):
    """
    Synchronizes parallel branches.
    """

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
        context,
    ):

        current = context.join_state.get(
            self.id,
            0,
        )

        current += 1

        context.join_state[self.id] = current

        #
        # Not all branches have arrived yet.
        #

        if current < self.expected:

            context.waiting = True

            return

        #
        # Reset state for future executions.
        #

        context.join_state.pop(
            self.id,
            None,
        )

        context.waiting = False