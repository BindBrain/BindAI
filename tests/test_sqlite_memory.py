from bindai_memory.providers.sqlite import SQLiteMemoryProvider
from bindai_memory.record import MemoryRecord


def test_sqlite_memory_set_get(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(
        str(db)
    )

    record = MemoryRecord(
        namespace="test",
        key="hello",
        value="world",
    )

    result = provider.set(record)

    assert result.success

    result = provider.get(
        "hello",
        "test",
    )

    assert result.success
    assert result.value.value == "world"

    provider.close()


def test_sqlite_memory_exists_delete_clear(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(
        str(db)
    )

    provider.set(
        MemoryRecord(
            namespace="test",
            key="a",
            value="123",
        )
    )

    assert provider.exists(
        "a",
        "test",
    )

    provider.delete(
        "a",
        "test",
    )

    assert not provider.exists(
        "a",
        "test",
    )

    provider.clear(
        "test",
    )

    provider.close()