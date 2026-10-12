from bindai_workflow.context import WorkflowContext
from bindai_workflow.nodes.loop import LoopNode


def test_loop_node_accepts_expression():
    node = LoopNode(
        node_id="loop",
        expression="count < 3",
    )

    assert node.expression == "count < 3"
    assert node.predicate is None


def test_loop_node_expression_selects_body():
    node = LoopNode(
        node_id="loop",
        expression="count < 3",
    )

    node.next_nodes = [
        "body",
        "exit",
    ]

    context = WorkflowContext()
    context.set("count", 1)

    node.execute(context)

    assert context.current_node == "body"


def test_loop_node_expression_selects_exit():
    node = LoopNode(
        node_id="loop",
        expression="count < 3",
    )

    node.next_nodes = [
        "body",
        "exit",
    ]

    context = WorkflowContext()
    context.set("count", 3)

    node.execute(context)

    assert context.current_node == "exit"


def test_loop_node_preserves_callable_predicate():
    node = LoopNode(
        node_id="loop",
        predicate=lambda context: True,
    )

    assert node.predicate is not None
    assert node.expression is None


def test_loop_node_requires_predicate_or_expression():
    try:
        LoopNode(
            node_id="loop",
        )
    except ValueError as exc:
        assert "predicate" in str(exc)
        assert "expression" in str(exc)
    else:
        raise AssertionError("LoopNode should require a predicate or expression.")
