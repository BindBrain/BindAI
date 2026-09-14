from __future__ import annotations

from datetime import UTC, datetime, timedelta

from bindai_workflow.context import WorkflowContext
from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.store import WorkflowStore
from bindai_workflow.timeout import TimeoutPolicy


class InMemoryStore(WorkflowStore):
    def __init__(self) -> None:
        self.instances = {}

    def save(self, instance: WorkflowInstance) -> None:
        self.instances[instance.id] = instance

    def load(self, instance_id: str) -> WorkflowInstance | None:
        return self.instances.get(instance_id)

    def delete(self, instance_id: str) -> None:
        self.instances.pop(instance_id, None)


def create_instance() -> WorkflowInstance:
    context = WorkflowContext()

    workflow = type(
        "Workflow",
        (),
        {
            "id": "test-workflow",
            "version": 1,
        },
    )()

    instance = WorkflowInstance(workflow)
    instance.context = context
    context.instance = instance

    return instance


def test_workflow_times_out_before_executing_next_node() -> None:
    instance = create_instance()

    instance.context.started_at = datetime.now(UTC) - timedelta(
        seconds=10,
    )
    instance.context.timeout_policy = TimeoutPolicy(
        seconds=5,
    )

    executor = WorkflowExecutor(
        InMemoryStore(),
    )

    result = executor._run(
        instance,
    )

    assert result.success is False
    assert result.error == "Workflow timeout."
    assert instance.context.completed is True
    assert instance.context.errors == ["Workflow timeout."]
    assert instance.context.finished_at is not None
    assert len(instance.context.events) == 1
    assert instance.context.events[0].type == "workflow.failed"


def test_workflow_without_timeout_policy_can_complete() -> None:
    instance = create_instance()

    executor = WorkflowExecutor(
        InMemoryStore(),
    )

    result = executor._run(
        instance,
    )

    assert result.success is True
    assert instance.context.completed is True
    assert instance.context.errors == []
    assert instance.context.finished_at is not None