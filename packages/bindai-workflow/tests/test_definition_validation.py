from bindai_workflow.definition import (
    WorkflowDefinition,
    WorkflowDefinitionValidator,
    WorkflowEdgeDefinition,
    WorkflowNodeDefinition,
)


def test_valid_decision_workflow_has_no_errors():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="decision",
                type="decision",
                configuration={
                    "expression": "approved == true",
                },
            ),
            WorkflowNodeDefinition(
                id="accepted",
                type="end",
            ),
            WorkflowNodeDefinition(
                id="rejected",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="decision",
            ),
            WorkflowEdgeDefinition(
                source="decision",
                target="accepted",
                port="true",
            ),
            WorkflowEdgeDefinition(
                source="decision",
                target="rejected",
                port="false",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    assert not [item for item in diagnostics if item.is_error]


def test_missing_start_is_reported():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="end",
                type="end",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    codes = {item.code for item in diagnostics}

    assert "workflow.missing_start" in codes


def test_decision_requires_both_branches():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="decision",
                type="decision",
                configuration={
                    "expression": "approved == true",
                },
            ),
            WorkflowNodeDefinition(
                id="accepted",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="decision",
            ),
            WorkflowEdgeDefinition(
                source="decision",
                target="accepted",
                port="true",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    codes = {item.code for item in diagnostics}

    assert "decision.missing_false_branch" in codes


def test_loop_requires_body_and_exit():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="loop",
                type="loop",
            ),
            WorkflowNodeDefinition(
                id="body",
                type="agent",
                configuration={"agent": "worker"},
            ),
            WorkflowNodeDefinition(
                id="exit",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="loop",
            ),
            WorkflowEdgeDefinition(
                source="loop",
                target="body",
                port="body",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    codes = {item.code for item in diagnostics}

    assert "loop.missing_exit_branch" in codes


def test_unknown_node_type_is_reported():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="mystery",
                type="something_new",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    codes = {item.code for item in diagnostics}

    assert "node.unknown_type" in codes


def test_unreachable_node_is_warning():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="end",
                type="end",
            ),
            WorkflowNodeDefinition(
                id="unused",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="end",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    unreachable = [
        item
        for item in diagnostics
        if item.code == "workflow.unreachable_node"
    ]

    assert len(unreachable) == 1
    assert unreachable[0].node_id == "unused"
    assert unreachable[0].is_warning
def test_human_approval_ports_are_valid():
    definition = WorkflowDefinition(
        id="test-human-approval",
        name="Human Approval Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="human-approval",
                type="human_task",
            ),
            WorkflowNodeDefinition(
                id="approved",
                type="end",
            ),
            WorkflowNodeDefinition(
                id="rejected",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="human-approval",
            ),
            WorkflowEdgeDefinition(
                source="human-approval",
                target="approved",
                port="approved",
            ),
            WorkflowEdgeDefinition(
                source="human-approval",
                target="rejected",
                port="rejected",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    assert not [
        item
        for item in diagnostics
        if item.code == "edge.unused_port"
    ]
    assert not [
        item
        for item in diagnostics
        if item.code == "edge.invalid_port"
    ]


def test_human_approval_rejects_unknown_port():
    definition = WorkflowDefinition(
        id="test-human-approval-invalid-port",
        name="Human Approval Invalid Port Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="human-approval",
                type="human_task",
            ),
            WorkflowNodeDefinition(
                id="end",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="human-approval",
            ),
            WorkflowEdgeDefinition(
                source="human-approval",
                target="end",
                port="unknown",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    invalid_ports = [
        item
        for item in diagnostics
        if item.code == "edge.invalid_port"
    ]

    assert len(invalid_ports) == 1
    assert invalid_ports[0].node_id == "human-approval"


def test_loop_requires_expression():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="loop",
                type="loop",
                configuration={},
            ),
            WorkflowNodeDefinition(
                id="body",
                type="end",
            ),
            WorkflowNodeDefinition(
                id="exit",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="loop",
            ),
            WorkflowEdgeDefinition(
                source="loop",
                target="body",
                port="body",
            ),
            WorkflowEdgeDefinition(
                source="loop",
                target="exit",
                port="exit",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(
        definition,
    )

    codes = {item.code for item in diagnostics}

    assert "node.missing_required_configuration" in codes

def test_condition_requires_expression():
    definition = WorkflowDefinition(
        id="test",
        name="Test",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="condition",
                type="condition",
                configuration={},
            ),
            WorkflowNodeDefinition(
                id="true-end",
                type="end",
            ),
            WorkflowNodeDefinition(
                id="false-end",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="condition",
            ),
            WorkflowEdgeDefinition(
                source="condition",
                target="true-end",
                port="true",
            ),
            WorkflowEdgeDefinition(
                source="condition",
                target="false-end",
                port="false",
            ),
        ],
    )

    diagnostics = WorkflowDefinitionValidator().validate(definition)

    codes = {item.code for item in diagnostics}

    assert "node.missing_required_configuration" in codes
