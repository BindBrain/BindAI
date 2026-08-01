from bindai_core import (
    AgentExecutor,
    AssistantAgent,
    ExecutionContext,
    ModelProvider,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "dummy"

    def generate(self, request):
        return ModelResponse(
            content="Hello from executor",
            usage=TokenUsage(),
        )


context = ExecutionContext()
context.variables.set("input", "Hello")


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

executor = AgentExecutor()

result = executor.execute(
    agent,
    context,
)

print(result.output)
