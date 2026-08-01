from bindai_memory import InMemoryProvider, Memory, MemoryRecord


def test_get_updates_access():

    memory = Memory(
        InMemoryProvider(),
    )

    memory.set(
        MemoryRecord(
            key="python",
            value="Python",
        )
    )

    result = memory.get(
        "python",
    )

    assert result.value.access_count == 1
    assert result.value.last_accessed is not None


def test_get_reinforces_memory():

    memory = Memory(
        InMemoryProvider(),
    )

    memory.set(
        MemoryRecord(
            key="python",
            value="Python",
        )
    )

    before = memory.get(
        "python",
    ).value.importance

    after = memory.get(
        "python",
    ).value.importance

    assert after > before
