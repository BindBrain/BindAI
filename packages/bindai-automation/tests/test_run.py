from datetime import UTC, datetime

from bindai_automation.run import AutomationRun


def test_run_has_initial_pending_state():
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    assert run.status == "pending"
    assert run.definition_id == "automation-1"
    assert run.definition_version == 1
    assert run.id
    assert isinstance(run.created_at, datetime)
    assert run.created_at.tzinfo == UTC
    assert run.started_at is None
    assert run.completed_at is None
    assert run.output is None
    assert run.error is None


def test_run_start_sets_running_state():
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    run.start()
    assert run.status == "running"
    assert run.started_at is not None
    assert run.started_at.tzinfo == UTC
    assert run.completed_at is None


def test_run_complete_sets_completed_state():
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    run.start()
    run.complete(output={"result": "done"})
    assert run.status == "completed"
    assert run.output == {"result": "done"}
    assert run.completed_at is not None
    assert run.completed_at.tzinfo == UTC
    assert run.error is None


def test_run_fail_sets_failed_state():
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    run.start()
    run.fail("execution failed")
    assert run.status == "failed"
    assert run.error == "execution failed"
    assert run.completed_at is not None
    assert run.completed_at.tzinfo == UTC


def test_run_accepts_input():
    input_data = {"message": "hello"}
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=2,
        input=input_data,
    )
    assert run.input == input_data
