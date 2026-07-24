from bindai_memory import Memory
from bindai_memory.record import MemoryRecord


def test_memory_search():

    memory = Memory()

    memory.set(
        MemoryRecord(
            key="1",
            value="BindAI is an agent framework",
        )
    )

    memory.set(
        MemoryRecord(
            key="2",
            value="Python workflow engine",
        )
    )

    results = memory.search("agent")

    assert len(results) == 1

    assert results[0].key == "1"