from bindai import Tool


def test_tool_success():

    tool = Tool(
        name="add",
        description="Adds numbers",
        function=lambda a, b: a + b,
    )

    result = tool(2, 3)

    assert result.success
    assert result.value == 5


def test_tool_exception():

    def fail():
        raise RuntimeError("boom")

    tool = Tool(
        name="fail",
        description="Fails",
        function=fail,
    )

    result = tool()

    assert not result.success
    assert result.error == "boom"