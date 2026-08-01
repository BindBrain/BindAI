from bindai_memory import (
    Memory,
    MemoryRecord,
)


def test_memory_delete_and_exists():

    memory = Memory(
        "memory",
    )

    memory.set(
        MemoryRecord(
            key="1",
            value="hello",
        )
    )

    assert memory.exists(
        "1",
    )

    memory.delete(
        "1",
    )

    assert not memory.exists(
        "1",
    )


def test_memory_clear():

    memory = Memory(
        "memory",
    )

    memory.set(
        MemoryRecord(
            key="1",
            value="hello",
        )
    )

    memory.clear()

    assert not memory.exists(
        "1",
    )


def test_vector_metadata_filter():

    memory = Memory(
        "vector",
    )

    memory.set(
        MemoryRecord(
            key="1",
            value="python programming",
            metadata={
                "topic": "code",
            },
        )
    )

    results = memory.search(
        "python",
        metadata={
            "topic": "code",
        },
    )

    assert len(results) == 1


def test_vector_search_limit():

    memory = Memory(
        "vector",
    )

    for i in range(5):

        memory.set(
            MemoryRecord(
                key=str(i),
                value="python",
            )
        )

    results = memory.search(
        "python",
        limit=2,
    )

    assert len(results) == 2