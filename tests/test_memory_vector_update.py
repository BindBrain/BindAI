from bindai_memory import (
    MemoryRecord,
    VectorMemoryProvider,
)


def test_vector_memory_update_replaces_record():

    memory = VectorMemoryProvider()

    memory.set(
        MemoryRecord(
            key="name",
            value="John",
        )
    )

    memory.set(
        MemoryRecord(
            key="name",
            value="Peter",
        )
    )

    result = memory.get(
        "name",
    )

    assert result.success is True
    assert result.value.value == "Peter"