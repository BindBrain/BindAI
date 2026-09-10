from bindai_memory.providers.sqlite import SQLiteMemoryProvider
from bindai_memory.record import MemoryRecord


def test_sqlite_memory_set_get(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(str(db))

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

    provider = SQLiteMemoryProvider(str(db))

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


def test_sqlite_memory_persists_across_instances(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(str(db))

    provider.set(
        MemoryRecord(
            namespace="test",
            key="persistent",
            value="stored value",
        )
    )

    provider.close()

    provider = SQLiteMemoryProvider(str(db))

    result = provider.get(
        "persistent",
        "test",
    )

    assert result.success
    assert result.value.value == "stored value"

    provider.close()


def test_sqlite_memory_search_metadata_filter(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(str(db))

    provider.set(
        MemoryRecord(
            namespace="test",
            key="python",
            value="Python programming",
            metadata={"language": "python"},
        )
    )

    provider.set(
        MemoryRecord(
            namespace="test",
            key="java",
            value="Java programming",
            metadata={"language": "java"},
        )
    )

    results = provider.search(
        query="programming",
        namespace="test",
        metadata={"language": "python"},
    )

    assert len(results) == 1
    assert results[0].key == "python"

    provider.close()


def test_sqlite_memory_search_namespace_isolation(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(str(db))

    provider.set(
        MemoryRecord(
            namespace="project-a",
            key="shared",
            value="Python project",
        )
    )

    provider.set(
        MemoryRecord(
            namespace="project-b",
            key="shared",
            value="Python project",
        )
    )

    results = provider.search(
        query="Python",
        namespace="project-a",
    )

    assert len(results) == 1
    assert results[0].namespace == "project-a"
    assert results[0].key == "shared"

    provider.close()


def test_sqlite_memory_expiration(tmp_path):
    db = tmp_path / "memory.db"

    provider = SQLiteMemoryProvider(str(db))

    from datetime import UTC, datetime, timedelta

    provider.set(
        MemoryRecord(
            namespace="test",
            key="expired",
            value="old value",
            expires_at=datetime.now(UTC) - timedelta(seconds=1),
        )
    )

    result = provider.get(
        "expired",
        "test",
    )

    assert not result.success

    assert not provider.exists(
        "expired",
        "test",
    )

    results = provider.search(
        query="old",
        namespace="test",
    )

    assert results == []

    provider.close()
