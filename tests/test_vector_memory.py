from bindai_memory import Memory
from bindai_memory.record import MemoryRecord


def test_vector_search():

    memory = Memory("vector")

    memory.set(
        MemoryRecord(
            key="1",
            value="BindAI agent framework",
        )
    )

    memory.set(
        MemoryRecord(
            key="2",
            value="Weather forecast",
        )
    )

    results = memory.search(
        "agent",
    )

    assert len(results) == 2

    assert results[0].score >= results[1].score
