from bindai_memory.manager import MemoryManager
from bindai_memory.record import MemoryRecord


def test_decay_reduces_importance():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
        importance=1.0,
    )

    manager.decay(
        record,
    )

    assert record.importance == 0.95


def test_decay_never_negative():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
        importance=0.01,
    )

    manager.decay(
        record,
        amount=1.0,
    )

    assert record.importance == 0.0


def test_forget_delegates():

    manager = MemoryManager()

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    assert (
        manager.forget(
            record,
        )
        is False
    )
