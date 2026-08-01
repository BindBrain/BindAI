from bindai_memory.record import MemoryRecord


def test_add_relation():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_relation(
        "django",
    )

    assert "django" in record.related_keys


def test_remove_relation():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_relation(
        "django",
    )

    record.remove_relation(
        "django",
    )

    assert "django" not in record.related_keys


def test_relation_not_duplicated():

    record = MemoryRecord(
        key="python",
        value="Python",
    )

    record.add_relation(
        "django",
    )

    record.add_relation(
        "django",
    )

    assert record.related_keys == [
        "django",
    ]
