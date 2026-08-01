from bindai_memory.memory import Memory
from bindai_memory.providers.sqlite import SQLiteMemoryProvider
from bindai_memory.record import MemoryRecord


def test_memory_default_provider():

    memory = Memory()

    record = MemoryRecord(
        namespace="test",
        key="hello",
        value="world",
    )

    result = memory.set(record)

    assert result.success

    result = memory.get(
        "hello",
        "test",
    )

    assert result.success
    assert result.value.value == "world"


def test_memory_set_get():

    memory = Memory()

    memory.set(
        MemoryRecord(
            namespace="test",
            key="name",
            value="BindAI",
        )
    )

    result = memory.get(
        "name",
        "test",
    )

    assert result.success
    assert result.value.value == "BindAI"


def test_memory_exists_delete():

    memory = Memory()

    memory.set(
        MemoryRecord(
            namespace="test",
            key="framework",
            value="BindAI",
        )
    )

    assert memory.exists(
        "framework",
        "test",
    )

    result = memory.delete(
        "framework",
        "test",
    )

    assert result.success

    assert not memory.exists(
        "framework",
        "test",
    )


def test_memory_clear():

    memory = Memory()

    memory.set(
        MemoryRecord(
            namespace="test",
            key="a",
            value="123",
        )
    )

    memory.set(
        MemoryRecord(
            namespace="test",
            key="b",
            value="456",
        )
    )

    result = memory.clear(
        "test",
    )

    assert result.success

    assert not memory.exists(
        "a",
        "test",
    )

    assert not memory.exists(
        "b",
        "test",
    )


def test_sqlite_provider():

    provider = SQLiteMemoryProvider(
        ":memory:",
    )

    memory = Memory(provider)

    try:
        result = memory.set(
            MemoryRecord(
                key="framework",
                value="BindAI",
            )
        )

        assert result.success

        result = memory.get(
            "framework",
        )

        assert result.success
        assert result.value.value == "BindAI"

        assert memory.exists(
            "framework",
        )

        result = memory.delete(
            "framework",
        )

        assert result.success

        assert not memory.exists(
            "framework",
        )

    finally:
        provider.close()


def test_sqlite_provider_search():

    provider = SQLiteMemoryProvider(
        ":memory:",
    )

    memory = Memory(provider)

    try:
        memory.set(
            MemoryRecord(
                namespace="test",
                key="language",
                value="Python",
            )
        )

        memory.set(
            MemoryRecord(
                namespace="test",
                key="framework",
                value="BindAI",
            )
        )

        results = memory.search(
            "Python",
            "test",
        )

        assert len(results) == 1
        assert results[0].value == "Python"

    finally:
        provider.close()
