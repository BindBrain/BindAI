from bindai_workflow import (
    DecisionNode,
    EndNode,
    HumanTaskNode,
    JoinNode,
    ParallelNode,
    StartNode,
    SubWorkflowNode,
    Workflow,
    WorkflowFactory,
    WorkflowNodeFactory,
    WorkflowSerializer,
)


def create_workflow():
    workflow = Workflow(
        "serialization_test",
    )

    start = StartNode(
        "start",
        name="Start",
    )

    decision = DecisionNode(
        "decision",
        expression="value > 10",
        name="Check value",
    )

    human = HumanTaskNode(
        "human",
        assignee="reviewer",
        form="review_form",
        name="Human review",
    )

    parallel = ParallelNode(
        "parallel",
        name="Parallel work",
    )

    join = JoinNode(
        "join",
        expected=2,
        name="Join branches",
    )

    subworkflow = SubWorkflowNode(
        "subworkflow",
        workflow_id="child_workflow",
        name="Run child",
    )

    end = EndNode(
        "end",
        name="End",
    )

    workflow.add_node(start)
    workflow.add_node(decision)
    workflow.add_node(human)
    workflow.add_node(parallel)
    workflow.add_node(join)
    workflow.add_node(subworkflow)
    workflow.add_node(end)

    workflow.start_node = start.id

    start.next_nodes = [
        decision.id,
    ]

    decision.true_node = human.id
    decision.false_node = parallel.id

    parallel.next_nodes = [
        human.id,
        subworkflow.id,
    ]

    human.next_nodes = [
        join.id,
    ]

    subworkflow.next_nodes = [
        join.id,
    ]

    join.next_nodes = [
        end.id,
    ]

    return workflow


def test_workflow_serialization_round_trip():
    workflow = create_workflow()

    serializer = WorkflowSerializer()

    data = serializer.to_dict(
        workflow,
    )

    factory = WorkflowFactory(
        WorkflowNodeFactory(),
    )

    restored = factory.create(
        data,
    )

    assert restored.id == workflow.id
    assert restored.name == workflow.name
    assert restored.version == workflow.version
    assert restored.start_node == workflow.start_node

    assert set(restored.nodes) == set(
        workflow.nodes,
    )


def test_node_types_survive_round_trip():
    workflow = create_workflow()

    data = WorkflowSerializer().to_dict(
        workflow,
    )

    restored = WorkflowFactory(
        WorkflowNodeFactory(),
    ).create(
        data,
    )

    assert isinstance(
        restored.get("start"),
        StartNode,
    )

    assert isinstance(
        restored.get("decision"),
        DecisionNode,
    )

    assert isinstance(
        restored.get("human"),
        HumanTaskNode,
    )

    assert isinstance(
        restored.get("parallel"),
        ParallelNode,
    )

    assert isinstance(
        restored.get("join"),
        JoinNode,
    )

    assert isinstance(
        restored.get("subworkflow"),
        SubWorkflowNode,
    )

    assert isinstance(
        restored.get("end"),
        EndNode,
    )


def test_node_configuration_survives_round_trip():
    workflow = create_workflow()

    data = WorkflowSerializer().to_dict(
        workflow,
    )

    restored = WorkflowFactory(
        WorkflowNodeFactory(),
    ).create(
        data,
    )

    decision = restored.get(
        "decision",
    )

    assert decision.expression == "value > 10"
    assert decision.true_node == "human"
    assert decision.false_node == "parallel"

    human = restored.get(
        "human",
    )

    assert human.assignee == "reviewer"
    assert human.form == "review_form"

    join = restored.get(
        "join",
    )

    assert join.expected == 2

    subworkflow = restored.get(
        "subworkflow",
    )

    assert subworkflow.workflow_id == "child_workflow"


def test_connections_survive_round_trip():
    workflow = create_workflow()

    data = WorkflowSerializer().to_dict(
        workflow,
    )

    restored = WorkflowFactory(
        WorkflowNodeFactory(),
    ).create(
        data,
    )

    assert restored.get("start").next_nodes == [
        "decision",
    ]

    assert restored.get("human").next_nodes == [
        "join",
    ]

    assert restored.get("subworkflow").next_nodes == [
        "join",
    ]

    assert restored.get("join").next_nodes == [
        "end",
    ]


def test_json_round_trip():
    import json

    workflow = create_workflow()

    serializer = WorkflowSerializer()

    json_data = serializer.to_json(
        workflow,
    )

    restored = WorkflowFactory(
        WorkflowNodeFactory(),
    ).create(
        json.loads(
            json_data,
        ),
    )

    assert restored.name == "serialization_test"
    assert set(restored.nodes) == set(
        workflow.nodes,
    )
def test_loop_expression_survives_round_trip():
    from bindai_workflow import LoopNode

    workflow = Workflow(
        "loop_serialization",
    )

    start = StartNode("start")
    loop = LoopNode(
        "loop",
        expression="count < 3",
        name="Repeat",
    )
    body = EndNode("body")
    exit_node = EndNode("exit")

    workflow.add_node(start)
    workflow.add_node(loop)
    workflow.add_node(body)
    workflow.add_node(exit_node)

    workflow.start_node = start.id

    start.next_nodes = [
        loop.id,
    ]

    loop.next_nodes = [
        body.id,
        exit_node.id,
    ]

    data = WorkflowSerializer().to_dict(
        workflow,
    )

    restored = WorkflowFactory(
        WorkflowNodeFactory(),
    ).create(
        data,
    )

    restored_loop = restored.get(
        "loop",
    )

    assert restored_loop.expression == "count < 3"
    assert restored_loop.predicate is None
    assert restored_loop.name == "Repeat"
    assert restored_loop.next_nodes == [
        "body",
        "exit",
    ]

def test_loop_expression_serializes():
    from bindai_workflow import LoopNode

    loop = LoopNode(
        "loop",
        expression="count < 3",
        name="Repeat",
    )

    data = loop.to_dict()

    assert data["type"] == "LoopNode"
    assert data["expression"] == "count < 3"
