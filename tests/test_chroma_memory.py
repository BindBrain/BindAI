from datetime import UTC, datetime, timedelta

from bindai_memory.providers.chroma import ChromaMemoryProvider
from bindai_memory.record import MemoryRecord, MemoryType


def test_set_and_get(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    record = MemoryRecord(
        key="test-001",
        value="Hello Chroma",
        namespace="default",
        type=MemoryType.LONG_TERM,
        metadata={"category": "test"},
    )

    result = provider.set(record)

    assert result.success is True

    fetched = provider.get("test-001")

    assert fetched.success is True
    assert fetched.value.value == "Hello Chroma"
    assert fetched.value.metadata["category"] == "test"


def test_namespace_isolation(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    provider.set(
        MemoryRecord(
            key="shared-key",
            value="namespace-a",
            namespace="a",
        )
    )

    provider.set(
        MemoryRecord(
            key="shared-key",
            value="namespace-b",
            namespace="b",
        )
    )

    result_a = provider.get("shared-key", namespace="a")
    result_b = provider.get("shared-key", namespace="b")

    assert result_a.success is True
    assert result_b.success is True
    assert result_a.value.value == "namespace-a"
    assert result_b.value.value == "namespace-b"


def test_search_and_metadata_filter(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    provider.set(
        MemoryRecord(
            key="search-001",
            value="Python programming language",
            namespace="default",
            metadata={"category": "programming"},
        )
    )

    provider.set(
        MemoryRecord(
            key="search-002",
            value="Cooking recipes and food",
            namespace="default",
            metadata={"category": "cooking"},
        )
    )

    results = provider.search(
        "Python programming",
        metadata={"category": "programming"},
        limit=5,
    )

    assert len(results) >= 1
    assert results[0].key == "search-001"
    assert results[0].metadata["category"] == "programming"


def test_exists_and_delete(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    provider.set(
        MemoryRecord(
            key="delete-001",
            value="Delete me",
        )
    )

    assert provider.exists("delete-001") is True

    result = provider.delete("delete-001")

    assert result.success is True
    assert provider.exists("delete-001") is False


def test_clear_namespace(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    provider.set(
        MemoryRecord(
            key="clear-001",
            value="Clear me",
            namespace="clear-test",
        )
    )

    provider.set(
        MemoryRecord(
            key="keep-001",
            value="Keep me",
            namespace="keep-test",
        )
    )

    result = provider.clear("clear-test")

    assert result.success is True
    assert provider.exists("clear-001", namespace="clear-test") is False
    assert provider.exists("keep-001", namespace="keep-test") is True


def test_expiration(tmp_path):
    provider = ChromaMemoryProvider(
        path=str(tmp_path / "chroma"),
        collection_name="test_memory",
    )

    provider.set(
        MemoryRecord(
            key="expired-001",
            value="Expired",
            expires_at=datetime.now(UTC) - timedelta(seconds=1),
        )
    )

    assert provider.exists("expired-001") is False

    result = provider.get("expired-001")

    assert result.success is False