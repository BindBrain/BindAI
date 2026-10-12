from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowNodeDefinition:
    id: str
    type: str
    name: str | None = None
    configuration: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
        }

        if self.name is not None:
            data["name"] = self.name

        data.update(self.configuration)
        return data


@dataclass(slots=True)
class WorkflowEdgeDefinition:
    source: str
    target: str
    port: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "from": self.source,
            "to": self.target,
        }

        if self.port is not None:
            data["port"] = self.port

        return data


@dataclass(slots=True)
class WorkflowDefinition:
    id: str
    name: str
    version: int = 1
    nodes: list[WorkflowNodeDefinition] = field(default_factory=list)
    edges: list[WorkflowEdgeDefinition] = field(default_factory=list)

    def node(self, node_id: str) -> WorkflowNodeDefinition:
        for node in self.nodes:
            if node.id == node_id:
                return node

        raise KeyError(f"Unknown workflow node: {node_id}")

    def has_node(self, node_id: str) -> bool:
        return any(node.id == node_id for node in self.nodes)

    def add_node(self, node: WorkflowNodeDefinition) -> None:
        if self.has_node(node.id):
            raise ValueError(f"Duplicate workflow node id: {node.id}")

        self.nodes.append(node)

    def add_edge(self, edge: WorkflowEdgeDefinition) -> None:
        if not self.has_node(edge.source):
            raise ValueError(f"Workflow edge references unknown source node: {edge.source}")

        if not self.has_node(edge.target):
            raise ValueError(f"Workflow edge references unknown target node: {edge.target}")

        self.edges.append(edge)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "workflow": {
                "id": self.id,
                "name": self.name,
                "nodes": [node.to_dict() for node in self.nodes],
                "edges": [edge.to_dict() for edge in self.edges],
            },
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        *,
        strict: bool = True,
    ) -> WorkflowDefinition:
        if not isinstance(data, dict):
            raise ValueError("Workflow definition must be a mapping.")

        workflow_data = data.get("workflow")

        if not isinstance(workflow_data, dict):
            raise ValueError("Workflow definition must contain a 'workflow' mapping.")

        workflow_id = workflow_data.get("id")
        workflow_name = workflow_data.get("name")

        if not workflow_id:
            raise ValueError("Workflow definition is missing 'workflow.id'.")

        if not workflow_name:
            raise ValueError("Workflow definition is missing 'workflow.name'.")

        raw_nodes = workflow_data.get("nodes", [])

        if not isinstance(raw_nodes, list):
            raise ValueError("'workflow.nodes' must be a list.")

        nodes: list[WorkflowNodeDefinition] = []

        for index, raw_node in enumerate(raw_nodes):
            if not isinstance(raw_node, dict):
                raise ValueError(f"Workflow node at index {index} must be a mapping.")

            node_id = raw_node.get("id")
            node_type = raw_node.get("type")

            if not node_id:
                raise ValueError(f"Workflow node at index {index} is missing 'id'.")

            if not node_type:
                raise ValueError(f"Workflow node '{node_id}' is missing 'type'.")

            configuration = dict(raw_node)

            configuration.pop("id", None)
            configuration.pop("type", None)

            node_name = configuration.pop("name", None)

            nodes.append(
                WorkflowNodeDefinition(
                    id=str(node_id),
                    type=str(node_type),
                    name=str(node_name) if node_name is not None else None,
                    configuration=configuration,
                )
            )

        raw_edges = workflow_data.get("edges", [])

        if not isinstance(raw_edges, list):
            raise ValueError("'workflow.edges' must be a list.")

        edges: list[WorkflowEdgeDefinition] = []

        for index, raw_edge in enumerate(raw_edges):
            if not isinstance(raw_edge, dict):
                raise ValueError(f"Workflow edge at index {index} must be a mapping.")

            source = raw_edge.get("from")
            target = raw_edge.get("to")

            if not source:
                raise ValueError(f"Workflow edge at index {index} is missing 'from'.")

            if not target:
                raise ValueError(f"Workflow edge at index {index} is missing 'to'.")

            port = raw_edge.get("port")

            if port is not None:
                port = str(port).lower()

            edges.append(
                WorkflowEdgeDefinition(
                    source=str(source),
                    target=str(target),
                    port=port,
                )
            )

        definition = cls(
            id=str(workflow_id),
            name=str(workflow_name),
            version=int(data.get("version", 1)),
            nodes=nodes,
            edges=edges,
        )

        if strict:
            node_ids = {node.id for node in definition.nodes}

            for edge in definition.edges:
                if edge.source not in node_ids:
                    raise ValueError(f"Workflow edge references unknown source node: {edge.source}")

                if edge.target not in node_ids:
                    raise ValueError(f"Workflow edge references unknown target node: {edge.target}")

        return definition
