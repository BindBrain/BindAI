from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ModelProvider,
    ModelResponse,
    TokenUsage,
    ToolCall,
    Tool,
)


class DummyProvider(ModelProvider):
    @property
    def name(self):
        return "dummy"

    def generate(self, request):

        return ModelResponse(
            content="",
            usage=TokenUsage(),
            tool_call=ToolCall(
                name="greet",
                arguments={
                    "person_name": "BindAI",
                },
            ),
        )


class GreetingTool(Tool):
    @property
    def name(self):
        return "greet"

    def execute(self, person_name: str):
        from bindai_core import ToolResult

        return ToolResult(
            success=True,
            output=f"Hello {person_name}",
        )


context = ExecutionContext()

agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

agent.register_tool(
    GreetingTool(),
)

result = agent.execute(context)

print(result.output)
