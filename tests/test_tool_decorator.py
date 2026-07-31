from bindai import Tool, tool


def test_tool_decorator():

    @tool
    def add(a, b):
        """Adds numbers."""
        return a + b

    assert isinstance(add, Tool)

    result = add(2, 3)

    assert result.success
    assert result.value == 5


def test_custom_name():

    @tool(name="calculator")
    def add(a, b):
        return a + b

    assert add.name == "calculator"


def test_custom_description():

    @tool(description="My calculator")
    def add(a, b):
        return a + b

    assert add.description == "My calculator"


def test_docstring_description():

    @tool
    def hello():
        """Returns hello."""
        return "hello"

    assert hello.description == "Returns hello."
