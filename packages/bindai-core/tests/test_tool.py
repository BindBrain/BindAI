from bindai_core.tool import tool


@tool()
def add(a: int, b: int):
    """Add two numbers."""
    return a + b


def test_tool_execution():

    result = add.execute(
        a=2,
        b=3,
    )

    assert result.success
    assert result.output == 5


def test_tool_definition():

    definition = add.definition

    assert definition.name == "add"

    assert "a" in definition.parameters

    assert "b" in definition.parameters


def test_tool_description():

    assert add.description == "Add two numbers."
