from __future__ import annotations

from concurrent.futures import Future

from bindai_automation import (
    AutomationDefinition,
    MemoryAutomationRunHistory,
    MemoryAutomationStateStore,
)
from bindai_automation.worker import AutomationWorker
from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable, ExecutionResult


class SampleExecutable(Executable):
    def execute(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output="done",
        )


class FailingExecutable(Executable):
    def execute(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult(
            success=False,
            error="failed",
        )


class RaisingExecutable(Executable):
    def execute(self, context: ExecutionContext) -> ExecutionResult:
        raise RuntimeError("boom")


def make_definition(
    executable: Executable | None = None,
) -> AutomationDefinition:
    return AutomationDefinition(
        name="test-automation",
        target=executable or SampleExecutable(),
    )


def test_worker_uses_default_state_and_history_stores():
    worker = AutomationWorker()
    assert isinstance(
        worker.state_store,
        MemoryAutomationStateStore,
    )
    assert isinstance(
        worker.history,
        MemoryAutomationRunHistory,
    )
    worker.shutdown()


def test_worker_run_completes_automation():
    worker = AutomationWorker()
    definition = make_definition()
    run = worker.run(definition)
    assert run.definition_id == definition.id
    assert run.definition_version == definition.version
    assert run.status == "completed"
    assert run.output == "done"
    assert run.error is None
    assert run.started_at is not None
    assert run.completed_at is not None
    worker.shutdown()


def test_worker_run_persists_completed_state():
    state_store = MemoryAutomationStateStore()
    history = MemoryAutomationRunHistory()
    worker = AutomationWorker(
        state_store=state_store,
        history=history,
    )
    definition = make_definition()
    run = worker.run(definition)
    stored = state_store.load(run.id)
    assert stored is not None
    assert stored.id == run.id
    assert stored.status == "completed"
    assert stored.output == "done"
    worker.shutdown()


def test_worker_run_records_history():
    state_store = MemoryAutomationStateStore()
    history = MemoryAutomationRunHistory()
    worker = AutomationWorker(
        state_store=state_store,
        history=history,
    )
    definition = make_definition()
    run = worker.run(definition)
    recorded = history.get(run.id)
    assert recorded is not None
    assert recorded.id == run.id
    assert recorded.status == "completed"
    assert recorded.output == "done"
    worker.shutdown()


def test_worker_handles_failed_execution_result():
    worker = AutomationWorker()
    definition = make_definition(FailingExecutable())
    run = worker.run(definition)
    assert run.status == "failed"
    assert run.error == "failed"
    assert run.output is None
    assert run.completed_at is not None
    worker.shutdown()


def test_worker_handles_execution_exception():
    worker = AutomationWorker()
    definition = make_definition(RaisingExecutable())
    run = worker.run(definition)
    assert run.status == "failed"
    assert run.error == "boom"
    assert run.completed_at is not None
    worker.shutdown()


def test_worker_submit_returns_future():
    worker = AutomationWorker()
    definition = make_definition()
    future = worker.submit(definition)
    assert isinstance(future, Future)
    run = future.result(timeout=5)
    assert run.status == "completed"
    assert run.output == "done"
    worker.shutdown()


def test_worker_submit_persists_initial_state():
    state_store = MemoryAutomationStateStore()
    worker = AutomationWorker(
        state_store=state_store,
    )
    definition = make_definition()
    future = worker.submit(definition)
    run = future.result(timeout=5)
    stored = state_store.load(run.id)
    assert stored is not None
    assert stored.id == run.id
    assert stored.status == "completed"
    worker.shutdown()


def test_worker_submit_records_history():
    history = MemoryAutomationRunHistory()
    worker = AutomationWorker(
        history=history,
    )
    definition = make_definition()
    future = worker.submit(definition)
    run = future.result(timeout=5)
    recorded = history.get(run.id)
    assert recorded is not None
    assert recorded.status == "completed"
    assert recorded.output == "done"
    worker.shutdown()


def test_worker_can_execute_multiple_automations():
    worker = AutomationWorker(max_workers=2)
    definition_one = make_definition()
    definition_two = make_definition()
    future_one = worker.submit(definition_one)
    future_two = worker.submit(definition_two)
    run_one = future_one.result(timeout=5)
    run_two = future_two.result(timeout=5)
    assert run_one.status == "completed"
    assert run_two.status == "completed"
    assert run_one.id != run_two.id
    worker.shutdown()


def test_worker_rejects_invalid_worker_count():
    try:
        AutomationWorker(max_workers=0)
    except ValueError as exc:
        assert str(exc) == "max_workers must be at least 1."
    else:
        raise AssertionError("Expected ValueError")


def test_worker_shutdown():
    worker = AutomationWorker()
    worker.shutdown()
    definition = make_definition()
    try:
        worker.submit(definition)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Expected RuntimeError after worker shutdown.")
