from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class NodeField:
    name: str
    type: str
    required: bool = False
    default: Any = None


@dataclass(frozen=True, slots=True)
class NodeCapability:
    type: str
    label: str
    category: str
    configuration: tuple[NodeField, ...] = field(default_factory=tuple)
    connection_mode: str = "single"

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "label": self.label,
            "category": self.category,
            "configuration": [
                {
                    "name": field.name,
                    "type": field.type,
                    "required": field.required,
                    "default": field.default,
                }
                for field in self.configuration
            ],
            "connection_mode": self.connection_mode,
        }


class WorkflowCapabilityRegistry:
    def __init__(self):
        self._capabilities: dict[str, NodeCapability] = {}

    def register(self, capability: NodeCapability) -> None:
        self._capabilities[capability.type] = capability

    def get(self, node_type: str) -> NodeCapability:
        return self._capabilities[node_type]

    def contains(self, node_type: str) -> bool:
        return node_type in self._capabilities

    def all(self) -> list[NodeCapability]:
        return list(self._capabilities.values())

    def to_dict(self) -> list[dict]:
        return [capability.to_dict() for capability in self._capabilities.values()]


def create_default_capability_registry() -> WorkflowCapabilityRegistry:
    registry = WorkflowCapabilityRegistry()

    registry.register(
        NodeCapability(
            type="StartNode",
            label="Start",
            category="Control",
            connection_mode="single",
        )
    )

    registry.register(
        NodeCapability(
            type="EndNode",
            label="End",
            category="Control",
            connection_mode="none",
        )
    )

    registry.register(
        NodeCapability(
            type="AgentNode",
            label="Agent",
            category="AI",
            configuration=(
                NodeField(
                    name="agent",
                    type="agent",
                    required=True,
                ),
                NodeField(
                    name="input_variable",
                    type="string",
                    default="input",
                ),
                NodeField(
                    name="output_variable",
                    type="string",
                    default="agent_output",
                ),
                NodeField(
                    name="input_mapping",
                    type="string",
                    default="",
                ),
            ),
            connection_mode="single",
        )
    )

    registry.register(
        NodeCapability(
            type="ToolNode",
            label="Tool",
            category="Execution",
            configuration=(
                NodeField(
                    name="tool",
                    type="tool",
                    required=True,
                ),
                NodeField(
                    name="output_variable",
                    type="string",
                    default="tool_output",
                ),
            ),
            connection_mode="single",
        )
    )

    registry.register(
        NodeCapability(
            type="ConditionNode",
            label="Condition",
            category="Control",
            configuration=(
                NodeField(
                    name="expression",
                    type="expression",
                    required=True,
                ),
            ),
            connection_mode="true_false",
        )
    )

    registry.register(
        NodeCapability(
            type="DecisionNode",
            label="Decision",
            category="Control",
            configuration=(
                NodeField(
                    name="expression",
                    type="expression",
                    required=True,
                ),
            ),
            connection_mode="true_false",
        )
    )

    registry.register(
        NodeCapability(
            type="ParallelNode",
            label="Parallel",
            category="Control",
            connection_mode="branches",
        )
    )

    registry.register(
        NodeCapability(
            type="JoinNode",
            label="Join",
            category="Control",
            configuration=(
                NodeField(
                    name="expected",
                    type="integer",
                    required=True,
                ),
            ),
            connection_mode="single",
        )
    )

    registry.register(
        NodeCapability(
            type="LoopNode",
            label="Loop",
            category="Control",
            configuration=(
                NodeField(
                    name="expression",
                    type="expression",
                    required=True,
                ),
            ),
            connection_mode="body_exit",
        )
    )

    registry.register(
        NodeCapability(
            type="SubWorkflowNode",
            label="Subworkflow",
            category="Control",
            configuration=(
                NodeField(
                    name="workflow_id",
                    type="workflow",
                    required=True,
                ),
            ),
            connection_mode="single",
        )
    )

    registry.register(
        NodeCapability(
            type="HumanTaskNode",
            label="Human Approval",
            category="Human",
            configuration=(
                NodeField(
                    name="assignee",
                    type="string",
                    required=False,
                ),
                NodeField(
                    name="form",
                    type="string",
                    required=False,
                ),
            ),
            connection_mode="approval",
        )
    )

    return registry


default_capability_registry = create_default_capability_registry()
