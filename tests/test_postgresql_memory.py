from bindai_memory.providers.postgresql import PostgreSQLMemoryProvider
from bindai_memory.record import MemoryRecord


def test_postgresql_memory_set_get():
    provider = PostgreSQLMemoryProvider("postgresql://postgres:postgres@localhost:5432/bindai")

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


def test_postgresql_memory_persists_across_instances():
    database = "postgresql://postgres:postgres@localhost:5432/bindai"

    provider = PostgreSQLMemoryProvider(database)

    provider.set(
        MemoryRecord(
            namespace="test",
            key="persistent",
            value="stored value",
        )
    )

    provider.close()

    provider = PostgreSQLMemoryProvider(database)

    result = provider.get(
        "persistent",
        "test",
    )

    assert result.success
    assert result.value.value == "stored value"

    provider.close()


def test_postgresql_memory_search_metadata_filter():
    database = "postgresql://postgres:postgres@localhost:5432/bindai"

    provider = PostgreSQLMemoryProvider(database)

    provider.clear("test")

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


def test_postgresql_memory_search_namespace_isolation():
    database = "postgresql://postgres:postgres@localhost:5432/bindai"

    provider = PostgreSQLMemoryProvider(database)

    provider.clear("project-a")
    provider.clear("project-b")

    provider.set(
        MemoryRecord(
            namespace="project-a",
            key="shared",
            value="Python project A",
        )
    )

    provider.set(
        MemoryRecord(
            namespace="project-b",
            key="shared",
            value="Python project B",
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


def test_postgresql_memory_expiration():
    from datetime import UTC, datetime, timedelta

    database = "postgresql://postgres:postgres@localhost:5432/bindai"

    provider = PostgreSQLMemoryProvider(database)

    provider.clear("test")

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
