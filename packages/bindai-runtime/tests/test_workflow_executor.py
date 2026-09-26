from __future__ import annotations

from bindai_core import ExecutionContext
from bindai_runtime.workflow_executor import WorkflowExecutor
from bindai_workflow import EndNode, StartNode, Workflow


def make_workflow() -> Workflow:
    workflow = Workflow(
        name="runtime-test",
    )

    start = StartNode(
        node_id="start",
    )

    end = EndNode(
        node_id="end",
    )

    start.next_nodes.append(
        "end",
    )

    workflow.add_node(
        start,
    )

    workflow.add_node(
        end,
    )

    return workflow


def test_runtime_workflow_executor_uses_workflow_executor() -> None:
    workflow = make_workflow()

    context = ExecutionContext()

    context.variables.set(
        "input",
        "hello",
    )

    executor = WorkflowExecutor(
        workflow,
    )

    result = executor.execute(
        context,
    )

    assert result.success is True
    assert result.output.get("input") == "hello"
    assert context.variables.get("input") == "hello"