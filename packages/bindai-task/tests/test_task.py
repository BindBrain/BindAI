from dataclasses import dataclass

from bindai_core.context import ExecutionContext
from bindai_task import Task, TaskResult, TaskState


@dataclass
class Response:
    output: str


class FakeAgent:
    def __init__(
        self,
        response=None,
        error: Exception | None = None,
    ):
        self.response = response
        self.error = error
        self.messages: list[str] = []

    def chat(self, message: str):
        self.messages.append(message)

        if self.error is not None:
            raise self.error

        return self.response


def make_task(
    agent: FakeAgent,
    *,
    expected_output: str | None = None,
) -> Task:
    return Task(
        description="Complete this task.",
        agent=agent,
        expected_output=expected_output,
    )


def test_task_starts_pending_without_result():
    agent = FakeAgent()
    task = make_task(agent)

    assert task.description == "Complete this task."
    assert task.agent is agent
    assert task.expected_output is None
    assert task.state == TaskState.PENDING
    assert task.result is None


def test_task_execute_calls_agent_with_description():
    agent = FakeAgent(response="done")
    task = make_task(agent)

    task.execute(ExecutionContext())

    assert agent.messages == ["Complete this task."]


def test_task_execute_returns_success_for_string_response():
    agent = FakeAgent(response="Task completed.")
    task = make_task(agent)

    result = task.execute(ExecutionContext())

    assert isinstance(result, TaskResult)
    assert result.success is True
    assert result.output == "Task completed."
    assert result.error is None
    assert task.result is result
    assert task.state == TaskState.COMPLETED


def test_task_execute_uses_response_output_attribute():
    agent = FakeAgent(
        response=Response(
            output="Structured output.",
        )
    )
    task = make_task(agent)

    result = task.execute(ExecutionContext())

    assert result.success is True
    assert result.output == "Structured output."
    assert task.state == TaskState.COMPLETED


def test_task_execute_sets_running_before_completion():
    states: list[TaskState] = []

    class TrackingAgent:
        def chat(self, message: str):
            states.append(task.state)
            return "done"

    task = Task(
        description="Complete this task.",
        agent=TrackingAgent(),
    )

    task.execute(ExecutionContext())

    assert states == [TaskState.RUNNING]
    assert task.state == TaskState.COMPLETED


def test_task_execute_returns_failure_when_agent_raises():
    agent = FakeAgent(
        error=RuntimeError("agent failed"),
    )
    task = make_task(agent)

    result = task.execute(ExecutionContext())

    assert isinstance(result, TaskResult)
    assert result.success is False
    assert result.output is None
    assert result.error == "agent failed"
    assert task.result is result
    assert task.state == TaskState.FAILED


def test_task_preserves_expected_output():
    agent = FakeAgent(response="done")
    task = make_task(
        agent,
        expected_output="A completed result",
    )

    assert task.expected_output == "A completed result"


def test_task_states_have_expected_values():
    assert TaskState.PENDING == "pending"
    assert TaskState.RUNNING == "running"
    assert TaskState.COMPLETED == "completed"
    assert TaskState.FAILED == "failed"