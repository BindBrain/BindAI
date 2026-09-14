from bindai_workflow import WorkflowBuilder
from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.memory_store import MemoryWorkflowStore
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.human import HumanTaskNode


class RecordingNode(WorkflowNode):
    def __init__(
        self,
        node_id: str,
        executed: list[str],
    ) -> None:
        super().__init__(
            node_id=node_id,
        )

        self.executed = executed

    def execute(
        self,
        context,
    ):
        self.executed.append(
            self.id,
        )

        return context


def test_human_task_pauses_workflow_until_approved() -> None:
    executed = []

    human = HumanTaskNode(
        node_id="review",
        assignee="reviewer@example.com",
    )

    after = RecordingNode(
        node_id="after",
        executed=executed,
    )

    workflow = (
        WorkflowBuilder("human-review")
        .start_node()
        .then(human)
        .then(after)
        .end_node()
        .build()
    )

    instance = workflow.create_instance()

    executor = WorkflowExecutor(
        MemoryWorkflowStore(),
    )

    result = executor.execute(
        instance,
    )

    assert result.success is True
    assert instance.context.waiting is True
    assert instance.context.task is not None
    assert instance.context.task.assignee == "reviewer@example.com"
    assert instance.context.task.completed is False
    assert executed == []

    instance.context.task.approve()

    result = executor.resume(
        instance,
    )

    assert result.success is True
    assert instance.context.waiting is False
    assert instance.context.task.completed is True
    assert instance.context.task.result == "approved"
    assert executed == ["after"]


def test_human_task_can_be_rejected_and_workflow_resumes() -> None:
    executed = []

    human = HumanTaskNode(
        node_id="review",
    )

    after = RecordingNode(
        node_id="after",
        executed=executed,
    )

    workflow = (
        WorkflowBuilder("human-review")
        .start_node()
        .then(human)
        .then(after)
        .end_node()
        .build()
    )

    instance = workflow.create_instance()

    executor = WorkflowExecutor(
        MemoryWorkflowStore(),
    )

    result = executor.execute(
        instance,
    )

    assert result.success is True
    assert instance.context.waiting is True
    assert executed == []

    instance.context.task.reject()

    result = executor.resume(
        instance,
    )

    assert result.success is True
    assert instance.context.waiting is False
    assert instance.context.task.completed is True
    assert instance.context.task.result == "rejected"
    assert executed == ["after"]


def test_resume_requires_waiting_workflow() -> None:
    workflow = (
        WorkflowBuilder("human-review")
        .start_node()
        .end_node()
        .build()
    )

    instance = workflow.create_instance()

    executor = WorkflowExecutor(
        MemoryWorkflowStore(),
    )

    try:
        executor.resume(
            instance,
        )
    except RuntimeError as exc:
        assert str(exc) == "Workflow is not waiting."
    else:
        raise AssertionError(
            "Expected RuntimeError when workflow is not waiting."
        )