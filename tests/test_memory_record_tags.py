from bindai_memory.record import MemoryRecord


def test_add_tag():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_tag(
        "language",
    )

    assert "language" in record.tags


def test_duplicate_tag():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_tag(
        "language",
    )

    record.add_tag(
        "language",
    )

    assert (
        len(
            record.tags,
        )
        == 1
    )


def test_remove_tag():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_tag(
        "language",
    )

    record.remove_tag(
        "language",
    )

    assert record.tags == []


def test_serializes_tags():

    record = MemoryRecord(
        key="python",
        value="Python",
        tags=[
            "language",
            "coding",
        ],
        source="docs",
    )

    data = record.to_dict()

    restored = MemoryRecord.from_dict(
        data,
    )

    assert restored.tags == [
        "language",
        "coding",
    ]

    assert restored.source == "docs"
