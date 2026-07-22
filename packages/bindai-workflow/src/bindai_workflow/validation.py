from __future__ import annotations

from .workflow import Workflow


class WorkflowValidator:
    """
    Validates workflow structure.
    """

    def validate(
        self,
        workflow: Workflow,
    ) -> list[str]:

        errors = []

        #
        # Must have start node
        #

        if workflow.start_node is None:
            errors.append("Workflow has no start node.")

        #
        # Every next node must exist
        #

        for node in workflow.nodes.values():
            for next_node in node.next_nodes:
                if next_node not in workflow.nodes:
                    errors.append(
                        f"Node '{node.id}' references missing node '{next_node}'."
                    )

        return errors
