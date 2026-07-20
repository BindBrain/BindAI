from bindai_memory import (
    Memory,
    MemoryRecord,
    MemoryRegistry,
)

from bindai_memory.providers import (
    InMemoryProvider,
    SQLiteMemoryProvider,
)


def test_default_memory():

    memory = Memory()

    assert isinstance(
        memory.provider,
        InMemoryProvider,
    )


def test_registry():

    provider = MemoryRegistry.provider(
        "memory",
    )

    assert provider is InMemoryProvider

    provider = MemoryRegistry.provider(
        "sqlite",
    )

    assert provider is SQLiteMemoryProvider


def test_set_get():

    memory = Memory()

    memory.set(

        MemoryRecord(

            key="name",

            value="BindAI",
        )
    )

    result = memory.get(
        "name",
    )

    assert result.success

    assert result.value.value == "BindAI"


def test_exists():

    memory = Memory()

    memory.set(

        MemoryRecord(

            key="language",

            value="Python",
        )
    )

    assert memory.exists(
        "language",
    )


def test_delete():

    memory = Memory()

    memory.set(

        MemoryRecord(

            key="temp",

            value="123",
        )
    )

    memory.delete(
        "temp",
    )

    assert not memory.exists(
        "temp",
    )


def test_clear():

    memory = Memory()

    memory.set(
        MemoryRecord(
            key="a",
            value="1",
        )
    )

    memory.set(
        MemoryRecord(
            key="b",
            value="2",
        )
    )

    memory.clear()

    assert not memory.exists("a")
    assert not memory.exists("b")


def test_sqlite_provider():

    memory = Memory(
        SQLiteMemoryProvider(
            ":memory:",
        )
    )

    memory.set(

        MemoryRecord(

            key="framework",

            value="BindAI",
        )
    )

    result = memory.get(
        "framework",
    )

    assert result.success

    assert result.value.value == "BindAI"