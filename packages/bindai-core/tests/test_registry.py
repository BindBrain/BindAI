from bindai_core.registry import Registry


def test_register():

    registry = Registry()

    registry.register(
        "one",
        123,
    )

    assert registry.get("one") == 123


def test_contains():

    registry = Registry()

    registry.register(
        "hello",
        "world",
    )

    assert registry.contains("hello")


def test_remove():

    registry = Registry()

    registry.register(
        "x",
        1,
    )

    registry.remove("x")

    assert not registry.contains("x")


def test_duplicate_registration():

    registry = Registry()

    registry.register(
        "value",
        1,
    )

    try:

        registry.register(
            "value",
            2,
        )

        assert False

    except ValueError:

        assert True


def test_clear():

    registry = Registry()

    registry.register(
        "a",
        1,
    )

    registry.clear()

    assert len(registry) == 0