from bindai_automation.history import AutomationRunHistory
from bindai_automation.run import AutomationRun


def test_history_is_abstract():
    assert AutomationRunHistory.__abstractmethods__ == {
        "record",
        "get",
        "list",
    }


def test_run_can_be_recorded_and_retrieved():
    from bindai_automation.memory_history import MemoryAutomationRunHistory

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


def test_history_lists_runs_in_insertion_order():
    from bindai_automation.memory_history import MemoryAutomationRunHistory

    history = MemoryAutomationRunHistory()

    first = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )
    second = AutomationRun(
        definition_id="automation-2",
        definition_version=3,
    )

    history.record(first)
    history.record(second)

    runs = history.list()

    assert [run.id for run in runs] == [first.id, second.id]


def test_history_returns_none_for_unknown_run():
    from bindai_automation.memory_history import MemoryAutomationRunHistory

    history = MemoryAutomationRunHistory()

    assert history.get("missing-run") is None


def test_history_stores_a_snapshot():
    from bindai_automation.memory_history import MemoryAutomationRunHistory

    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
        output="original",
    )

    history.record(run)
    run.output = "changed"

    stored = history.get(run.id)

    assert stored is not None
    assert stored.output == "original"


def test_history_returns_independent_snapshots():
    from bindai_automation.memory_history import MemoryAutomationRunHistory

    history = MemoryAutomationRunHistory()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
        output={"value": "original"},
    )

    history.record(run)

    stored = history.get(run.id)
    assert stored is not None

    stored.output["value"] = "changed"

    latest = history.get(run.id)

    assert latest is not None
    assert latest.output == {"value": "original"}