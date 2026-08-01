from bindai_memory.manager import MemoryManager
from bindai_memory.record import (
    MemoryRecord,
    MemoryType,
)


def test_memory_promotes_after_repeated_access():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.access_count = 5

    promoted = manager.promote(
        record,
    )

    assert promoted is True
    assert record.type == MemoryType.SEMANTIC


def test_memory_not_promoted():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    promoted = manager.promote(
        record,
    )

    assert promoted is False
    assert record.type == MemoryType.LONG_TERM
