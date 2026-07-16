from bindai_core import (
    AssistantAgent,
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


agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

print(agent.name)

print(agent.instructions)

print(agent.configuration.temperature)