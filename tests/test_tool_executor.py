from bindai import Tool
from bindai import ToolExecutor
from bindai import ToolRegistry


def test_execute():

    registry = ToolRegistry()

    registry.register(
        Tool(
            name="add",
            description="Adds",
            function=lambda a, b: a + b,
        )
    )

    executor = ToolExecutor(registry)

    result = executor.execute(
        "add",
        2,
        5,
    )

    assert result.success
    assert result.value == 7


def test_unknown_tool():

    executor = ToolExecutor(ToolRegistry())

    result = executor.execute("missing")

    assert not result.success
    assert "Unknown tool" in result.error


def test_exception():

    registry = ToolRegistry()

    def fail():
        raise RuntimeError("boom")

    registry.register(
        Tool(
            "fail",
            "Fails",
            fail,
        )
    )

    executor = ToolExecutor(registry)

    result = executor.execute("fail")

    assert not result.success
    assert result.error == "boom"
