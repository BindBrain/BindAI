from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ExecutionPipeline,
    ExecutionRequest,
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
            content="ExecutionResponse works!",
            usage=TokenUsage(),
        )


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

context = ExecutionContext()
context.variables.set("input", "Hello")

request = ExecutionRequest(
    agent=agent,
    context=context,
)

pipeline = ExecutionPipeline()

response = pipeline.execute(request)

print(response.result.output)