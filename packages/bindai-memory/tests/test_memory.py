from datetime import UTC, datetime, timedelta

from bindai_memory import (
    InMemoryProvider,
    MemoryManager,
    MemoryRecord,
    MemoryType,
)


def test_memory_record_supports_tags_and_relationships():
    record = MemoryRecord(
        key="user",
        value="Alice",
        type="short_term",
    )

    assert record.type is MemoryType.SHORT_TERM

    record.add_tag("important")
    record.add_tag("important")

    assert record.has_tag("important")
    assert record.tags == ["important"]

    record.remove_tag("important")

    assert not record.has_tag("important")

    record.add_relationship("related", "profile")
    record.add_relationship("related", "profile")
    record.add_relationship("depends_on", "account")

    assert record.get_relationships("related") == ["profile"]
    assert record.get_relationships("depends_on") == ["account"]
    assert record.related_keys == ["profile"]

    record.remove_relation("profile")

    assert not record.has_relation("profile")
    assert record.get_relationships("related") == []


def test_memory_record_round_trips_through_dict():
    created_at = datetime(2026, 1, 1, tzinfo=UTC)
    updated_at = datetime(2026, 1, 2, tzinfo=UTC)

    record = MemoryRecord(
        key="session",
        value={"message": "hello"},
        namespace="chat",
        type=MemoryType.EPISODIC,
        metadata={"source": "test"},
        importance=1.5,
        access_count=3,
        embedding=[0.1, 0.2],
        score=0.8,
        tags=["chat"],
        source="unit-test",
        relationships={"related": ["other"]},
        created_at=created_at,
        updated_at=updated_at,
    )

    restored = MemoryRecord.from_dict(record.to_dict())

    assert restored.key == record.key
    assert restored.value == record.value
    assert restored.namespace == record.namespace
    assert restored.type is MemoryType.EPISODIC
    assert restored.metadata == record.metadata
    assert restored.importance == record.importance
    assert restored.access_count == record.access_count
    assert restored.embedding == record.embedding
    assert restored.score == record.score
    assert restored.tags == record.tags
    assert restored.source == record.source
    assert restored.relationships == record.relationships
    assert restored.related_keys == record.related_keys
    assert restored.created_at == created_at
    assert restored.updated_at == updated_at


def test_memory_manager_promotes_high_importance_memory():
    manager = MemoryManager()
    record = MemoryRecord(
        key="important",
        value="remember this",
        importance=2.0,
    )

    assert manager.should_promote(record)
    assert manager.promote(record)
    assert record.type is MemoryType.SEMANTIC

    assert not manager.promote(record)


def test_memory_manager_promotes_frequently_accessed_memory():
    manager = MemoryManager()
    record = MemoryRecord(
        key="frequent",
        value="often used",
        access_count=5,
    )

    assert manager.should_promote(record)
    assert manager.promote(record)
    assert record.type is MemoryType.SEMANTIC


def test_memory_manager_handles_expiration_and_decay():
    manager = MemoryManager()
    record = MemoryRecord(
        key="temporary",
        value="expires",
        importance=0.1,
        expires_at=datetime.now(UTC) - timedelta(seconds=1),
    )

    assert manager.should_forget(record)
    assert manager.forget(record)

    manager.decay(record, amount=0.5)

    assert record.importance == 0.0

    manager.set_expiration(record, days=1)

    assert record.expires_at is not None
    assert record.expires_at > datetime.now(UTC)

    manager.clear_expiration(record)

    assert record.expires_at is None


def test_in_memory_provider_supports_namespaces_and_crud():
    provider = InMemoryProvider()

    record = MemoryRecord(
        key="item",
        value="hello",
        namespace="one",
    )

    result = provider.set(record)

    assert result.success
    assert result.value is not record
    assert provider.exists("item", "one")
    assert not provider.exists("item", "two")

    fetched = provider.get("item", "one")

    assert fetched.success
    assert fetched.value is not record
    assert fetched.value.value == "hello"

    missing = provider.get("item", "two")

    assert not missing.success

    deleted = provider.delete("item", "one")

    assert deleted.success
    assert not provider.exists("item", "one")


def test_in_memory_provider_searches_and_filters_metadata():
    provider = InMemoryProvider()

    provider.set(
        MemoryRecord(
            key="one",
            value="Python programming",
            metadata={"topic": "python"},
        )
    )
    provider.set(
        MemoryRecord(
            key="two",
            value="Python testing",
            metadata={"topic": "testing"},
        )
    )
    provider.set(
        MemoryRecord(
            key="three",
            value="Java programming",
            metadata={"topic": "java"},
        )
    )

    results = provider.search(
        "python",
        metadata={"topic": "python"},
    )

    assert [record.key for record in results] == ["one"]

    limited = provider.search(
        "python",
        limit=1,
    )

    assert len(limited) == 1

    assert provider.search("python", limit=0) == []


def test_in_memory_provider_ignores_expired_records():
    provider = InMemoryProvider()

    provider.set(
        MemoryRecord(
            key="expired",
            value="old",
            expires_at=datetime.now(UTC) - timedelta(seconds=1),
        )
    )

    assert not provider.exists("expired")

    result = provider.get("expired")

    assert not result.success

    assert provider.search("old") == []


def test_in_memory_provider_clear_removes_only_namespace():
    provider = InMemoryProvider()

    provider.set(
        MemoryRecord(
            key="one",
            value="value",
            namespace="one",
        )
    )
    provider.set(
        MemoryRecord(
            key="two",
            value="value",
            namespace="two",
        )
    )

    result = provider.clear("one")

    assert result.success
    assert not provider.exists("one", "one")
    assert provider.exists("two", "two")