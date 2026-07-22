from bindai_core import (
    AssistantAgent,
    Tool,
    ToolResult,
    ModelProvider,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):
    @property
    def name(self):
        return "dummy"

    def generate(self, request):
        return ModelResponse(
            content="ok",
            usage=TokenUsage(),
        )


class GreetingTool(Tool):
    """
    Simple greeting tool.
    """

    @property
    def name(self) -> str:
        return "greet"

    def execute(self, **kwargs) -> ToolResult:

        name = kwargs.get("name", "World")

        return ToolResult(
            success=True,
            output=f"Hello {name}",
        )


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

agent.register_tool(GreetingTool())

result = agent.execute_tool(
    "greet",
    name="BindAI",
)

print(result.output)
