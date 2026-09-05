from __future__ import annotations

import time

from dotenv import load_dotenv

from bindai_memory import MemoryRecord
from bindai_memory.providers import PineconeMemoryProvider


load_dotenv()


TEST_NAMESPACE = "bindai-automated-test"


def provider() -> PineconeMemoryProvider:
    return PineconeMemoryProvider()


def test_pinecone_set_get():
    p = provider()

    record = MemoryRecord(
        key="test-set-get",
        value="BindAI Pinecone test",
        namespace=TEST_NAMESPACE,
        metadata={"category": "test"},
    )

    result = p.set(record)
    assert result.success

    time.sleep(5)

    result = p.get(
        "test-set-get",
        TEST_NAMESPACE,
    )

    assert result.success
    assert result.value is not None
    assert result.value.key == "test-set-get"
    assert result.value.value == "BindAI Pinecone test"
    assert result.value.namespace == TEST_NAMESPACE
    assert result.value.metadata == {"category": "test"}


def test_pinecone_search_and_metadata_filter():
    p = provider()

    p.set(
        MemoryRecord(
            key="test-search-ai",
            value="Python AI application",
            namespace=TEST_NAMESPACE,
            metadata={"category": "ai"},
        )
    )

    p.set(
        MemoryRecord(
            key="test-search-database",
            value="Python database application",
            namespace=TEST_NAMESPACE,
            metadata={"category": "database"},
        )
    )

    time.sleep(5)

    results = p.search(
        "Python application",
        namespace=TEST_NAMESPACE,
        limit=10,
        metadata={"meta__category": "ai"},
    )

    keys = [record.key for record in results]

    assert "test-search-ai" in keys
    assert "test-search-database" not in keys


def test_pinecone_exists_and_delete():
    p = provider()

    p.set(
        MemoryRecord(
            key="test-delete",
            value="Delete me",
            namespace=TEST_NAMESPACE,
        )
    )

    time.sleep(5)

    assert p.exists(
        "test-delete",
        TEST_NAMESPACE,
    )

    result = p.delete(
        "test-delete",
        TEST_NAMESPACE,
    )

    assert result.success

    # Pinecone deletion is eventually consistent.
    time.sleep(5)

    assert not p.exists(
        "test-delete",
        TEST_NAMESPACE,
    )


def test_pinecone_clear():
    p = provider()

    p.set(
        MemoryRecord(
            key="test-clear-1",
            value="Clear me",
            namespace=TEST_NAMESPACE,
        )
    )

    p.set(
        MemoryRecord(
            key="test-clear-2",
            value="Clear me too",
            namespace=TEST_NAMESPACE,
        )
    )

    time.sleep(5)

    assert p.exists(
        "test-clear-1",
        TEST_NAMESPACE,
    )

    assert p.exists(
        "test-clear-2",
        TEST_NAMESPACE,
    )

    result = p.clear(TEST_NAMESPACE)

    assert result.success

    time.sleep(5)

    stats = p._index.describe_index_stats()

    assert TEST_NAMESPACE not in stats.namespaces