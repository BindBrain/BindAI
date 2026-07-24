from __future__ import annotations

from ..node import WorkflowNode


class LoopNode(WorkflowNode):
    """
    Repeats execution while predicate returns True.

    next_nodes[0] = loop body
    next_nodes[1] = exit node
    """

    def __init__(
        self,
        node_id: str,
        predicate,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.predicate = predicate

    def execute(
        self,
        context,
    ):

        if len(self.next_nodes) < 2:
            raise RuntimeError(
                "LoopNode requires two next nodes "
                "(body and exit)."
            )

        #
        # Continue loop
        #

        if self.predicate(
            context,
        ):

            context.current_node = self.next_nodes[0]

        #
        # Exit loop
        #

        else:

            context.current_node = self.next_nodes[1]