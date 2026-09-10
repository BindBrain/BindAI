import time

from bindai import GroupBuilder, Task
from bindai_agent.result import AgentResult
from bindai_group.processes import ParallelProcess


class FakeAgent:
    def __init__(self, name, output, delay=0):
        self.name = name
        self.output = output
        self.delay = delay
        self.started = None
        self.finished = None

    def execute(self, context):
        self.started = time.monotonic()

        if self.delay:
            time.sleep(self.delay)

        self.finished = time.monotonic()

        return AgentResult(
            success=True,
            output=self.output,
        )


def test_parallel_process_runs_independent_tasks_concurrently():
    first = FakeAgent("First", "first", delay=0.2)
    second = FakeAgent("Second", "second", delay=0.2)

    first_task = Task(
        description="First task",
        agent=first,
    )

    second_task = Task(
        description="Second task",
        agent=second,
    )

    group = (
        GroupBuilder()
        .agent(first)
        .agent(second)
        .task(first_task)
        .task(second_task)
        .process(ParallelProcess())
        .build()
    )

    started = time.monotonic()
    result = group.run()
    elapsed = time.monotonic() - started

    assert result.success
    assert group.state.value == "completed"

    assert first.started is not None
    assert second.started is not None
    assert abs(first.started - second.started) < 0.15
    assert elapsed < 0.35


def test_parallel_process_respects_dependencies():
    first = FakeAgent("Researcher", "research result", delay=0.1)
    second = FakeAgent("Writer", "summary", delay=0.1)

    research = Task(
        description="Research the topic.",
        agent=first,
    )

    summary = Task(
        description="Summarize the research.",
        agent=second,
    ).context_from(research)

    group = (
        GroupBuilder()
        .agent(first)
        .agent(second)
        .task(research)
        .task(summary)
        .process(ParallelProcess())
        .build()
    )

    result = group.run()

    assert result.success
    assert research.result is not None
    assert summary.result is not None
    assert second.started >= first.finished


def test_parallel_process_preserves_task_order_in_output():
    first = FakeAgent("First", "first", delay=0.2)
    second = FakeAgent("Second", "second", delay=0.01)

    first_task = Task(
        description="First task",
        agent=first,
    )

    second_task = Task(
        description="Second task",
        agent=second,
    )

    group = (
        GroupBuilder()
        .agent(first)
        .agent(second)
        .task(first_task)
        .task(second_task)
        .process(ParallelProcess())
        .build()
    )

    result = group.run()

    assert result.success
    assert result.output == "first\n\nsecond"


def test_parallel_process_fails_when_task_fails():
    class FailingAgent:
        name = "Failing"

        def execute(self, context):
            return AgentResult(
                success=False,
                error="expected failure",
            )

    agent = FailingAgent()

    task = Task(
        description="Fail",
        agent=agent,
    )

    group = (
        GroupBuilder()
        .agent(agent)
        .task(task)
        .process(ParallelProcess())
        .build()
    )

    result = group.run()

    assert not result.success
    assert result.error == "expected failure"
    assert group.state.value == "failed"


def test_parallel_process_handles_multiple_dependency_levels():
    researcher = FakeAgent("Researcher", "research", delay=0.05)
    analyst = FakeAgent("Analyst", "analysis", delay=0.05)
    writer = FakeAgent("Writer", "report", delay=0.05)

    research = Task(
        description="Research.",
        agent=researcher,
    )

    analysis = Task(
        description="Analyze.",
        agent=analyst,
    ).context_from(research)

    report = Task(
        description="Write report.",
        agent=writer,
    ).context_from(research, analysis)

    group = (
        GroupBuilder()
        .agent(researcher)
        .agent(analyst)
        .agent(writer)
        .task(research)
        .task(analysis)
        .task(report)
        .process(ParallelProcess())
        .build()
    )

    result = group.run()

    assert result.success
    assert research.result is not None
    assert analysis.result is not None
    assert report.result is not None

    assert researcher.finished <= analyst.started
    assert analyst.finished <= writer.started


def test_parallel_process_does_not_run_dependent_task_after_failure():
    class FailingAgent:
        name = "Failing"

        def execute(self, context):
            return AgentResult(
                success=False,
                error="research failed",
            )

    class TrackingAgent:
        name = "Dependent"

        def __init__(self):
            self.executed = False

        def execute(self, context):
            self.executed = True

            return AgentResult(
                success=True,
                output="should not run",
            )

    failing = FailingAgent()
    dependent = TrackingAgent()

    research = Task(
        description="Research.",
        agent=failing,
    )

    analysis = Task(
        description="Analyze the research.",
        agent=dependent,
    ).context_from(research)

    group = (
        GroupBuilder()
        .agent(failing)
        .agent(dependent)
        .task(research)
        .task(analysis)
        .process(ParallelProcess())
        .build()
    )

    result = group.run()

    assert not result.success
    assert result.error == "research failed"
    assert not dependent.executed
    assert group.state.value == "failed"