from __future__ import annotations

from bindai_workflow.context import WorkflowContext
from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.node import WorkflowNode
from bindai_workflow.retry import RetryPolicy
from bindai_workflow.store import WorkflowStore


class InMemoryStore(WorkflowStore):
    def __init__(self) -> None:
        self.instances = {}

    def save(self, instance: WorkflowInstance) -> None:
        self.instances[instance.id] = instance

    def load(self, instance_id: str) -> WorkflowInstance | None:
        return self.instances.get(instance_id)

    def delete(self, instance_id: str) -> None:
        self.instances.pop(instance_id, None)


class FailingNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("failing")
        self.attempts = 0

    def execute(self, context: WorkflowContext) -> WorkflowContext:
        self.attempts += 1
        raise RuntimeError("node failed")


class EventuallySuccessfulNode(WorkflowNode):
    def __init__(self, failures_before_success: int) -> None:
        super().__init__("eventually-successful")
        self.failures_before_success = failures_before_success
        self.attempts = 0

    def execute(self, context: WorkflowContext) -> WorkflowContext:
        self.attempts += 1

        if self.attempts <= self.failures_before_success:
            raise RuntimeError("temporary failure")

        return context


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


def test_failing_node_retries_until_max_attempts() -> None:
    node = FailingNode()
    instance = create_instance()

    instance.context.retry_policy = RetryPolicy(
        max_attempts=3,
    )

    executor = WorkflowExecutor(
        InMemoryStore(),
    )

    result = executor._execute_node(
        instance,
        node,
    )

    assert result is not None
    assert result.success is False
    assert result.error == "node failed"
    assert node.attempts == 3


def test_node_stops_retrying_after_success() -> None:
    node = EventuallySuccessfulNode(
        failures_before_success=2,
    )
    instance = create_instance()

    instance.context.retry_policy = RetryPolicy(
        max_attempts=3,
    )

    executor = WorkflowExecutor(
        InMemoryStore(),
    )

    result = executor._execute_node(
        instance,
        node,
    )

    assert result is None
    assert node.attempts == 3
    assert instance.context.retry_attempt == 0

def test_node_runs_once_without_retry_policy() -> None:
    node = FailingNode()
    instance = create_instance()

    executor = WorkflowExecutor(
        InMemoryStore(),
    )

    result = executor._execute_node(
        instance,
        node,
    )

    assert result is not None
    assert result.success is False
    assert result.error == "node failed"
    assert node.attempts == 1