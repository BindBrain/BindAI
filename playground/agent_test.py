from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ModelProvider,
    ModelRequest,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):
    @property
    def name(self):
        return "dummy"

    def generate(self, request: ModelRequest):

        return ModelResponse(
            content="Hello from AssistantAgent!",
            usage=TokenUsage(),
        )


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

context = ExecutionContext()

context.variables.set("input", "Hello")

result = agent.execute(context)

print(result.success)
print(result.output)
