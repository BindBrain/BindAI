from bindai_automation import AutomationRun, MemoryAutomationRunHistory


def test_history_starts_empty():
    history = MemoryAutomationRunHistory()

    assert history.list() == ()


def test_record_stores_run():
    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )

    history.record(run)

    stored = history.get(run.id)

    assert stored is not None
    assert stored.id == run.id
    assert stored.definition_id == "automation-1"
    assert stored.definition_version == 1


def test_record_preserves_run_state():
    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=2,
        input={"message": "hello"},
    )

    run.start()
    run.complete(output={"result": "done"})

    history.record(run)

    stored = history.get(run.id)

    assert stored is not None
    assert stored.status == "completed"
    assert stored.input == {"message": "hello"}
    assert stored.output == {"result": "done"}
    assert stored.started_at == run.started_at
    assert stored.completed_at == run.completed_at


def test_record_creates_snapshot():
    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
        output={"result": "original"},
    )

    history.record(run)

    run.output = {"result": "changed"}

    stored = history.get(run.id)

    assert stored is not None
    assert stored.output == {"result": "original"}


def test_get_returns_independent_snapshot():
    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
        output={"result": "original"},
    )

    history.record(run)

    first = history.get(run.id)
    assert first is not None

    first.output["result"] = "changed"

    second = history.get(run.id)

    assert second is not None
    assert second.output == {"result": "original"}


def test_list_returns_runs_in_insertion_order():
    history = MemoryAutomationRunHistory()

    first = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    second = AutomationRun(
        definition_id="automation-2",
        definition_version=3,
    )
    third = AutomationRun(
        definition_id="automation-3",
        definition_version=2,
    )

    history.record(first)
    history.record(second)
    history.record(third)

    runs = history.list()

    assert [run.id for run in runs] == [
        first.id,
        second.id,
        third.id,
    ]


def test_get_unknown_run_returns_none():
    history = MemoryAutomationRunHistory()

    assert history.get("missing-run") is None