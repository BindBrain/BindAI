from pathlib import Path

import pytest

from bindai_workflow.context import WorkflowContext
from bindai_workflow.definition import (
    WorkflowDefinition,
    WorkflowDefinitionLoader,
    WorkflowDefinitionRuntime,
)
from bindai_workflow.nodes.human import HumanTaskNode
from bindai_workflow.nodes.loop import LoopNode


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "visual_workflow.yaml"
)


def test_load_visual_workflow_definition():
    loader = WorkflowDefinitionLoader()

    definition = loader.load(FIXTURE)

    assert definition.id == "visual-test"
    assert definition.name == "Visual Test"
    assert definition.version == 1

    assert [node.id for node in definition.nodes] == [
        "start",
        "decision",
        "accepted",
        "rejected",
    ]

    assert len(definition.edges) == 3

    assert definition.edges[1].port == "true"
    assert definition.edges[2].port == "false"


def test_visual_definition_builds_runtime_workflow():
    loader = WorkflowDefinitionLoader()
    runtime = WorkflowDefinitionRuntime()

    definition = loader.load(FIXTURE)
    workflow = runtime.build(definition)

    assert workflow.id == "visual-test"
    assert workflow.name == "Visual Test"
    assert workflow.version == 1
    assert workflow.start_node == "start"

    decision = workflow.get("decision")

    assert decision.true_node == "accepted"
    assert decision.false_node == "rejected"

def test_workflow_definition_can_load_non_strictly() -> None:
    definition = WorkflowDefinition.from_dict(
        {
            "version": 1,
            "workflow": {
                "id": "broken",
                "name": "Broken Workflow",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "missing",
                    },
                ],
            },
        },
        strict=False,
    )

    assert definition.id == "broken"
    assert len(definition.edges) == 1
    assert definition.edges[0].target == "missing"


def test_workflow_definition_strict_loading_rejects_unknown_node() -> None:
    with pytest.raises(ValueError, match="unknown target node"):
        WorkflowDefinition.from_dict(
            {
                "version": 1,
                "workflow": {
                    "id": "broken",
                    "name": "Broken Workflow",
                    "nodes": [
                        {
                            "id": "start",
                            "type": "start",
                        },
                    ],
                    "edges": [
                        {
                            "from": "start",
                            "to": "missing",
                        },
                    ],
                },
            },
        )

def test_human_task_definition_builds_approval_branches() -> None:
    definition = WorkflowDefinition.from_dict(
        {
            "version": 1,
            "workflow": {
                "id": "human-approval",
                "name": "Human Approval",
                "nodes": [
                    {
                        "id": "start",
                        "type": "StartNode",
                    },
                    {
                        "id": "review",
                        "type": "HumanTaskNode",
                        "name": "Human Approval",
                        "assignee": "reviewer@example.com",
                    },
                    {
                        "id": "approved",
                        "type": "EndNode",
                    },
                    {
                        "id": "rejected",
                        "type": "EndNode",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "review",
                    },
                    {
                        "from": "review",
                        "to": "approved",
                        "port": "approved",
                    },
                    {
                        "from": "review",
                        "to": "rejected",
                        "port": "rejected",
                    },
                ],
            },
        },
    )

    runtime = WorkflowDefinitionRuntime()
    workflow = runtime.build(definition)

    assert workflow.start_node == "start"

    human = workflow.get("review")

    assert isinstance(human, HumanTaskNode)
    assert human.assignee == "reviewer@example.com"
    assert human.approved_node == "approved"
    assert human.rejected_node == "rejected"
def test_loop_definition_builds_from_expression():
    definition = WorkflowDefinition.from_dict(
        {
            "version": 1,
            "workflow": {
                "id": "loop-expression",
                "name": "Loop Expression",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                    {
                        "id": "loop",
                        "type": "loop",
                        "expression": "count < 3",
                    },
                    {
                        "id": "body",
                        "type": "end",
                    },
                    {
                        "id": "exit",
                        "type": "end",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "loop",
                    },
                    {
                        "from": "loop",
                        "to": "body",
                        "port": "body",
                    },
                    {
                        "from": "loop",
                        "to": "exit",
                        "port": "exit",
                    },
                ],
            },
        },
    )

    runtime = WorkflowDefinitionRuntime()
    workflow = runtime.build(definition)

    loop = workflow.get("loop")

    assert loop.expression == "count < 3"
    assert loop.predicate is None

def test_decision_definition_executes_expression():
    definition = WorkflowDefinition.from_dict(
        {
            "version": 1,
            "workflow": {
                "id": "decision-expression",
                "name": "Decision Expression",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                    },
                    {
                        "id": "decision",
                        "type": "decision",
                        "expression": 'classification == "true"',
                    },
                    {
                        "id": "true-end",
                        "type": "end",
                    },
                    {
                        "id": "false-end",
                        "type": "end",
                    },
                ],
                "edges": [
                    {
                        "from": "start",
                        "to": "decision",
                    },
                    {
                        "from": "decision",
                        "to": "true-end",
                        "port": "true",
                    },
                    {
                        "from": "decision",
                        "to": "false-end",
                        "port": "false",
                    },
                ],
            },
        },
    )

    runtime = WorkflowDefinitionRuntime()
    workflow = runtime.build(definition)

    for value in ("true", "false"):
        instance = workflow.create_instance()
        instance.context.set("classification", value)

        result = workflow.executor.execute(instance)

        assert result.success is True
        assert result.output["classification"] == value

def test_loop_expression_routes_to_body_or_exit():
    loop = LoopNode(
        node_id="loop",
        expression="count < 3",
    )
    loop.next_nodes = ["body", "exit"]

    context = WorkflowContext()
    context.set("count", 2)

    loop.execute(context)

    assert context.current_node == "body"

    context.current_node = None
    context.set("count", 3)

    loop.execute(context)

    assert context.current_node == "exit"
