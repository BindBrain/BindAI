from __future__ import annotations

from collections import defaultdict

from .diagnostics import DefinitionDiagnostic
from .models import WorkflowDefinition


class WorkflowDefinitionValidator:
    """
    Validate a portable workflow definition without resolving runtime
    dependencies such as agents, tools, or Python callables.
    """

    _KNOWN_TYPES = {
        "start",
        "startnode",
        "end",
        "endnode",
        "agent",
        "agentnode",
        "tool",
        "toolnode",
        "decision",
        "decisionnode",
        "condition",
        "conditionnode",
        "parallel",
        "parallelnode",
        "join",
        "joinnode",
        "loop",
        "loopnode",
        "human_task",
        "humantask",
        "humantasknode",
        "subworkflow",
        "subworkflownode",
    }

    def validate(
        self,
        definition: WorkflowDefinition,
    ) -> list[DefinitionDiagnostic]:
        diagnostics: list[DefinitionDiagnostic] = []

        self._validate_workflow_structure(definition, diagnostics)
        self._validate_nodes(definition, diagnostics)
        self._validate_edges(definition, diagnostics)
        self._validate_reachability(definition, diagnostics)

        return diagnostics

    def _validate_workflow_structure(
        self,
        definition: WorkflowDefinition,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        if not definition.id.strip():
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.missing_id",
                    message="Workflow is missing an id.",
                    suggestion="Give the workflow a stable unique id.",
                )
            )

        if not definition.name.strip():
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.missing_name",
                    message="Workflow is missing a name.",
                    suggestion="Give the workflow a human-readable name.",
                )
            )

        if definition.version < 1:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.invalid_version",
                    message="Workflow version must be at least 1.",
                    suggestion="Set workflow version to 1 or greater.",
                )
            )

        if not definition.nodes:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.empty",
                    message="Workflow contains no nodes.",
                    suggestion="Add at least a start and end node.",
                )
            )

        seen: set[str] = set()

        for node in definition.nodes:
            if node.id in seen:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="workflow.duplicate_node_id",
                        message=(
                            f"Workflow contains duplicate node id "
                            f"'{node.id}'."
                        ),
                        node_id=node.id,
                        node_type=node.type,
                        suggestion="Give every node a unique id.",
                    )
                )

            seen.add(node.id)

    def _validate_nodes(
        self,
        definition: WorkflowDefinition,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        start_nodes = []

        for node in definition.nodes:
            node_type = node.type.strip().lower()

            if node_type not in self._KNOWN_TYPES:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="node.unknown_type",
                        message=(
                            f"Node '{node.id}' uses unsupported type "
                            f"'{node.type}'."
                        ),
                        node_id=node.id,
                        node_type=node.type,
                        suggestion=(
                            "Choose a supported BindAI workflow node type."
                        ),
                    )
                )
                continue

            if node_type in {"start", "startnode"}:
                start_nodes.append(node)

            self._validate_node_configuration(
                node,
                node_type,
                diagnostics,
            )

        if not start_nodes:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.missing_start",
                    message="Workflow has no start node.",
                    suggestion="Add one start node.",
                )
            )

        if len(start_nodes) > 1:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="workflow.multiple_start_nodes",
                    message="Workflow contains multiple start nodes.",
                    suggestion="Keep exactly one start node.",
                )
            )

    def _validate_node_configuration(
        self,
        node,
        node_type: str,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        config = node.configuration

        if node_type in {"agent", "agentnode"}:
            self._require(node, "agent", diagnostics)

        elif node_type in {"tool", "toolnode"}:
            self._require(node, "tool", diagnostics)

        elif node_type in {"decision", "decisionnode"}:
            self._require(node, "expression", diagnostics)

        elif node_type in {"condition", "conditionnode"}:
            self._require(node, "expression", diagnostics)

        elif node_type in {"loop", "loopnode"}:
            self._require(
                node,
                "expression",
                diagnostics,
            )

        elif node_type in {"join", "joinnode"}:
            expected = config.get("expected")

            if expected is None:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="node.missing_required_configuration",
                        message=(
                            f"Join node '{node.id}' is missing "
                            "'expected'."
                        ),
                        node_id=node.id,
                        node_type=node.type,
                        suggestion=(
                            "Configure the number of branches the join "
                            "must wait for."
                        ),
                    )
                )
            else:
                try:
                    expected_value = int(expected)
                except (TypeError, ValueError):
                    expected_value = 0

                if expected_value < 1:
                    diagnostics.append(
                        DefinitionDiagnostic(
                            severity="error",
                            code="join.invalid_expected",
                            message=(
                                f"Join node '{node.id}' has invalid "
                                f"expected value '{expected}'."
                            ),
                            node_id=node.id,
                            node_type=node.type,
                            suggestion=(
                                "Set expected to a positive integer."
                            ),
                        )
                    )

        elif node_type in {
            "subworkflow",
            "subworkflownode",
        }:
            self._require(
                node,
                "workflow_id",
                diagnostics,
            )

    @staticmethod
    def _require(
        node,
        field_name: str,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        value = node.configuration.get(field_name)

        if value is None or str(value).strip() == "":
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code="node.missing_required_configuration",
                    message=(
                        f"Node '{node.id}' is missing required "
                        f"configuration '{field_name}'."
                    ),
                    node_id=node.id,
                    node_type=node.type,
                    suggestion=(
                        f"Configure '{field_name}' for this node."
                    ),
                )
            )

    def _validate_edges(
        self,
        definition: WorkflowDefinition,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        node_map = {node.id: node for node in definition.nodes}
        outgoing: dict[str, list] = defaultdict(list)

        for edge in definition.edges:
            source = node_map.get(edge.source)
            target = node_map.get(edge.target)

            if source is None:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="workflow.invalid_node_reference",
                        message=(
                            f"Edge references unknown source node "
                            f"'{edge.source}'."
                        ),
                        suggestion=(
                            "Connect the edge to an existing node."
                        ),
                    )
                )
                continue

            if target is None:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="workflow.invalid_node_reference",
                        message=(
                            f"Edge references unknown target node "
                            f"'{edge.target}'."
                        ),
                        node_id=source.id,
                        node_type=source.type,
                        suggestion=(
                            "Connect the edge to an existing node."
                        ),
                    )
                )
                continue

            outgoing[source.id].append(edge)

            self._validate_edge_port(
                source,
                edge.port,
                diagnostics,
            )

        for node in definition.nodes:
            node_type = node.type.strip().lower()
            edges = outgoing.get(node.id, [])

            if node_type in {
                "decision",
                "decisionnode",
                "condition",
                "conditionnode",
            }:
                self._require_branch(
                    node,
                    edges,
                    "true",
                    diagnostics,
                )
                self._require_branch(
                    node,
                    edges,
                    "false",
                    diagnostics,
                )

            elif node_type in {"loop", "loopnode"}:
                self._require_branch(
                    node,
                    edges,
                    "body",
                    diagnostics,
                )
                self._require_branch(
                    node,
                    edges,
                    "exit",
                    diagnostics,
                )

            elif node_type in {"parallel", "parallelnode"}:
                if len(edges) < 2:
                    diagnostics.append(
                        DefinitionDiagnostic(
                            severity="error",
                            code="parallel.insufficient_branches",
                            message=(
                                f"Parallel node '{node.id}' has fewer "
                                "than two outgoing branches."
                            ),
                            node_id=node.id,
                            node_type=node.type,
                            suggestion=(
                                "Connect the parallel node to at least "
                                "two branch nodes."
                            ),
                        )
                    )

    @staticmethod
    def _validate_edge_port(
        source,
        port: str | None,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        node_type = source.type.strip().lower()

        if node_type in {
            "decision",
            "decisionnode",
            "condition",
            "conditionnode",
        }:
            if port not in {"true", "false"}:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="edge.invalid_port",
                        message=(
                            f"Node '{source.id}' requires edge port "
                            "'true' or 'false'."
                        ),
                        node_id=source.id,
                        node_type=source.type,
                        suggestion=(
                            "Set the edge port to 'true' or 'false'."
                        ),
                    )
                )
            return

        if node_type in {"loop", "loopnode"}:
            if port not in {"body", "exit"}:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="edge.invalid_port",
                        message=(
                            f"Loop node '{source.id}' requires edge port "
                            "'body' or 'exit'."
                        ),
                        node_id=source.id,
                        node_type=source.type,
                        suggestion=(
                            "Set the edge port to 'body' or 'exit'."
                        ),
                    )
                )
            return

        if node_type in {
            "human_task",
            "humantask",
            "humantasknode",
        }:
            if port not in {"approved", "rejected"}:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="error",
                        code="edge.invalid_port",
                        message=(
                            f"Human approval node '{source.id}' requires "
                            "edge port 'approved' or 'rejected'."
                        ),
                        node_id=source.id,
                        node_type=source.type,
                        suggestion=(
                            "Set the edge port to 'approved' or 'rejected'."
                        ),
                    )
                )
            return
        if port is not None:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="warning",
                    code="edge.unused_port",
                    message=(
                        f"Edge port '{port}' is not used by node "
                        f"'{source.id}'."
                    ),
                    node_id=source.id,
                    node_type=source.type,
                    suggestion="Remove the unnecessary edge port.",
                )
            )

    @staticmethod
    def _require_branch(
        node,
        edges,
        port: str,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        matching = [
            edge
            for edge in edges
            if edge.port == port
        ]

        if not matching:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code=(
                        f"{node.type.strip().lower()}"
                        f".missing_{port}_branch"
                    ),
                    message=(
                        f"Node '{node.id}' is missing its "
                        f"'{port}' branch."
                    ),
                    node_id=node.id,
                    node_type=node.type,
                    suggestion=(
                        f"Connect the '{port}' output to another node."
                    ),
                )
            )
            return

        if len(matching) > 1:
            diagnostics.append(
                DefinitionDiagnostic(
                    severity="error",
                    code=(
                        f"{node.type.strip().lower()}"
                        f".multiple_{port}_branches"
                    ),
                    message=(
                        f"Node '{node.id}' has multiple "
                        f"'{port}' branches."
                    ),
                    node_id=node.id,
                    node_type=node.type,
                    suggestion=(
                        f"Keep exactly one '{port}' outgoing edge."
                    ),
                )
            )

    def _validate_reachability(
        self,
        definition: WorkflowDefinition,
        diagnostics: list[DefinitionDiagnostic],
    ) -> None:
        node_map = {node.id: node for node in definition.nodes}

        if not node_map:
            return

        start_nodes = [
            node
            for node in definition.nodes
            if node.type.strip().lower()
            in {"start", "startnode"}
        ]

        if len(start_nodes) != 1:
            return

        adjacency: dict[str, list[str]] = defaultdict(list)

        for edge in definition.edges:
            if (
                edge.source in node_map
                and edge.target in node_map
            ):
                adjacency[edge.source].append(edge.target)

        reachable: set[str] = set()
        queue = [start_nodes[0].id]

        while queue:
            node_id = queue.pop(0)

            if node_id in reachable:
                continue

            reachable.add(node_id)
            queue.extend(adjacency[node_id])

        for node in definition.nodes:
            if node.id not in reachable:
                diagnostics.append(
                    DefinitionDiagnostic(
                        severity="warning",
                        code="workflow.unreachable_node",
                        message=(
                            f"Node '{node.id}' is not reachable from "
                            "the workflow start node."
                        ),
                        node_id=node.id,
                        node_type=node.type,
                        suggestion=(
                            "Connect this node to the reachable "
                            "workflow graph or remove it."
                        ),
                    )
                )
