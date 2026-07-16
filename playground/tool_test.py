from bindai_core import (
    Tool,
    ToolResult,
    ToolRegistry,
)


class Calculator(Tool):

    @property
    def name(self):
        return "calculator"

    def execute(self, **kwargs):

        a = kwargs["a"]
        b = kwargs["b"]

        return ToolResult(
            output=a + b
        )


registry = ToolRegistry()

registry.register(
    Calculator()
)

tool = registry.get(
    "calculator"
)

result = tool.execute(
    a=10,
    b=15,
)

print(result.success)
print(result.output)
print(registry.names())
print(len(registry))