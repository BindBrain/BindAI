from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowDiagnostic:
    severity: str
    code: str
    message: str
    node_id: str | None = None
    node_type: str | None = None
    suggestion: str | None = None


class WorkflowValidator:
    def validate(self, workflow) -> list[WorkflowDiagnostic]:
        diagnostics: list[WorkflowDiagnostic] = []

        if not workflow.nodes:
            diagnostics.append(
                WorkflowDiagnostic(
                    severity="error",
                    code="workflow.empty",
                    message="Workflow has no nodes.",
                    suggestion="Add a Start node to the workflow.",
                )
            )
            return diagnostics

        if workflow.start_node is None:
            diagnostics.append(
                WorkflowDiagnostic(
                    severity="error",
                    code="workflow.missing_start",
                    message="Workflow has no start node.",
                    suggestion="Add a Start node to the workflow.",
                )
            )

        for node in workflow.nodes.values():
            for next_node in node.next_nodes:
                if next_node not in workflow.nodes:
                    diagnostics.append(
                        WorkflowDiagnostic(
                            severity="error",
                            code="workflow.invalid_node_reference",
                            message=(f"Node '{node.id}' references missing node '{next_node}'."),
                            node_id=node.id,
                            node_type=type(node).__name__,
                            suggestion=(
                                "Reconnect the node to an existing node "
                                "or remove the invalid connection."
                            ),
                        )
                    )

        return diagnostics
