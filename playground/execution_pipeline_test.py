from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ExecutionPipeline,
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
            content="Pipeline works!",
            usage=TokenUsage(),
        )


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

context = ExecutionContext()

context.variables.set(
    "input",
    "Hello",
)

pipeline = ExecutionPipeline()

result = pipeline.execute(
    agent,
    context,
)

print(result.result.output)
