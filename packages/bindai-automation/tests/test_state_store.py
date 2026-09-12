from bindai_automation.memory_store import MemoryAutomationStateStore
from bindai_automation.run import AutomationRun


def test_memory_store_saves_and_loads_run():
    store = MemoryAutomationStateStore()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )

    store.save(run)

    assert store.load(run.id) is run


def test_memory_store_returns_none_for_missing_run():
    store = MemoryAutomationStateStore()

    assert store.load("missing-run") is None


def test_memory_store_deletes_run():
    store = MemoryAutomationStateStore()
    run = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
    )

    store.save(run)
    store.delete(run.id)

    assert store.load(run.id) is None


def test_memory_store_replaces_existing_run():
    store = MemoryAutomationStateStore()
    first = AutomationRun(
        definition_id="automation-1",
        definition_version=1,
        id="run-1",
    )
    second = AutomationRun(
        definition_id="automation-2",
        definition_version=2,
        id="run-1",
    )

    store.save(first)
    store.save(second)

    assert store.load("run-1") is second
