from bindai_memory import MemoryRecord, MemoryType


def test_memory_record_serialization():

    record = MemoryRecord(
        key="user",
        value="John",
        type=MemoryType.SEMANTIC,
        metadata={
            "role": "developer",
        },
    )

    data = record.to_dict()

    restored = MemoryRecord.from_dict(
        data,
    )

    assert restored.key == "user"
    assert restored.value == "John"
    assert restored.type == MemoryType.SEMANTIC
    assert restored.metadata["role"] == "developer"


def test_memory_record_metadata_none():

    record = MemoryRecord(
        key="test",
        value="value",
        metadata=None,
    )

    assert record.metadata == {}


def test_memory_record_touch():

    record = MemoryRecord(
        key="test",
        value="value",
    )

    old = record.updated_at

    record.touch()

    assert record.updated_at >= old
