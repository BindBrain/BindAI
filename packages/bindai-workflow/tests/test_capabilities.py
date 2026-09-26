from bindai_workflow import (
    NodeCapability,
    NodeField,
    WorkflowCapabilityRegistry,
    default_capability_registry,
)


def test_default_registry_contains_core_nodes():
    expected = {
        "StartNode",
        "EndNode",
        "AgentNode",
        "ToolNode",
        "ConditionNode",
        "DecisionNode",
        "ParallelNode",
        "JoinNode",
        "LoopNode",
    }

    capabilities = {
        capability.type
        for capability in default_capability_registry.all()
    }

    assert expected.issubset(capabilities)


def test_agent_capability_matches_agent_node_configuration():
    capability = default_capability_registry.get(
        "AgentNode",
    )

    assert capability.label == "Agent"
    assert capability.category == "AI"
    assert capability.connection_mode == "single"

    fields = {
        field.name: field
        for field in capability.configuration
    }

    assert fields["agent"].type == "agent"
    assert fields["agent"].required is True

    assert fields["input_variable"].type == "string"
    assert fields["input_variable"].default == "input"

    assert fields["output_variable"].type == "string"
    assert fields["output_variable"].default == "agent_output"


def test_control_flow_connection_modes():
    assert (
        default_capability_registry.get(
            "ConditionNode",
        ).connection_mode
        == "true_false"
    )

    assert (
        default_capability_registry.get(
            "DecisionNode",
        ).connection_mode
        == "true_false"
    )

    assert (
        default_capability_registry.get(
            "ParallelNode",
        ).connection_mode
        == "branches"
    )

    assert (
        default_capability_registry.get(
            "LoopNode",
        ).connection_mode
        == "body_exit"
    )


def test_capability_serialization():
    capability = default_capability_registry.get(
        "AgentNode",
    )

    data = capability.to_dict()

    assert data["type"] == "AgentNode"
    assert data["label"] == "Agent"
    assert data["category"] == "AI"
    assert data["connection_mode"] == "single"

    assert data["configuration"] == [
        {
            "name": "agent",
            "type": "agent",
            "required": True,
            "default": None,
        },
        {
            "name": "input_variable",
            "type": "string",
            "required": False,
            "default": "input",
        },
        {
            "name": "output_variable",
            "type": "string",
            "required": False,
            "default": "agent_output",
        },
    ]


def test_custom_capability_registry():
    registry = WorkflowCapabilityRegistry()

    capability = NodeCapability(
        type="ExampleNode",
        label="Example",
        category="Test",
        configuration=(
            NodeField(
                name="value",
                type="string",
                required=True,
            ),
        ),
    )

    registry.register(capability)

    assert registry.contains("ExampleNode")
    assert registry.get("ExampleNode") is capability
    assert registry.all() == [capability]