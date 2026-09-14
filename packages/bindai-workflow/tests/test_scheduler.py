from datetime import UTC, datetime, timedelta

from bindai_workflow import WorkflowSchedule, WorkflowScheduler


def test_scheduler_returns_enabled_due_schedules() -> None:
    scheduler = WorkflowScheduler()

    due_schedule = WorkflowSchedule(
        workflow_id="due",
        next_run=datetime.now(UTC) - timedelta(seconds=1),
    )

    future_schedule = WorkflowSchedule(
        workflow_id="future",
        next_run=datetime.now(UTC) + timedelta(minutes=5),
    )

    disabled_schedule = WorkflowSchedule(
        workflow_id="disabled",
        next_run=datetime.now(UTC) - timedelta(seconds=1),
        enabled=False,
    )

    scheduler.add(due_schedule)
    scheduler.add(future_schedule)
    scheduler.add(disabled_schedule)

    due = scheduler.due()

    assert due == [due_schedule]


def test_scheduler_reschedules_recurring_schedule() -> None:
    next_run = datetime.now(UTC)

    schedule = WorkflowSchedule(
        workflow_id="workflow",
        next_run=next_run,
        interval_seconds=60,
    )

    scheduler = WorkflowScheduler()

    scheduler.reschedule(schedule)

    assert schedule.next_run == next_run + timedelta(
        seconds=60,
    )


def test_scheduler_does_not_change_one_shot_schedule() -> None:
    next_run = datetime.now(UTC)

    schedule = WorkflowSchedule(
        workflow_id="workflow",
        next_run=next_run,
    )

    scheduler = WorkflowScheduler()

    scheduler.reschedule(schedule)

    assert schedule.next_run == next_run