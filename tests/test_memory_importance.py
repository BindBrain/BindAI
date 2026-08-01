from bindai_memory.providers import VectorMemoryProvider
from bindai_memory.record import MemoryRecord


def test_importance_affects_ranking():

    memory = VectorMemoryProvider()

    memory.set(
        MemoryRecord(
            key="low",
            value="BindAI framework",
            importance=0.0,
        )
    )

    memory.set(
        MemoryRecord(
            key="high",
            value="BindAI framework",
            importance=1.0,
        )
    )

    results = memory.search(
        "BindAI",
    )

    assert results[0].key == "high"
