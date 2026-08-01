from datetime import UTC, datetime, timedelta

from bindai_memory.providers import VectorMemoryProvider
from bindai_memory.record import MemoryRecord


def test_recent_memory_ranks_higher():

    memory = VectorMemoryProvider()

    old = MemoryRecord(
        key="old",
        value="BindAI framework",
    )

    old.last_accessed = datetime.now(
        UTC,
    ) - timedelta(days=60)

    recent = MemoryRecord(
        key="recent",
        value="BindAI framework",
    )

    recent.last_accessed = datetime.now(
        UTC,
    )

    memory.set(old)
    memory.set(recent)

    results = memory.search(
        "BindAI",
    )

    assert results[0].key == "recent"
