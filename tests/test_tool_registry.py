from bindai import Tool, ToolRegistry


def test_register():

    registry = ToolRegistry()

    tool = Tool(
        name="add",
        description="Adds numbers",
        function=lambda a, b: a + b,
    )

    registry.register(tool)

    assert "add" in registry
    assert len(registry) == 1


def test_get():

    registry = ToolRegistry()

    tool = Tool(
        name="echo",
        description="Echo",
        function=lambda x: x,
    )

    registry.register(tool)

    assert registry.get("echo") is tool


def test_unregister():

    registry = ToolRegistry()

    tool = Tool(
        name="echo",
        description="Echo",
        function=lambda x: x,
    )

    registry.register(tool)

    registry.unregister("echo")

    assert "echo" not in registry


def test_list():

    registry = ToolRegistry()

    registry.register(
        Tool(
            name="a",
            description="A",
            function=lambda: None,
        )
    )

    registry.register(
        Tool(
            name="b",
            description="B",
            function=lambda: None,
        )
    )

    assert len(registry.list()) == 2
