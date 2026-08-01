from bindai_memory import MemoryManager, MemoryRecord


def test_memory_manager_touch():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    manager.touch(
        record,
    )

    assert record.access_count == 1
    assert record.last_accessed is not None


def test_memory_manager_reinforce():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    previous = record.importance

    manager.reinforce(
        record,
    )

    assert record.importance > previous


def test_memory_manager_promote():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
        importance=2.5,
    )

    assert manager.should_promote(
        record,
    )
