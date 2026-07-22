from bindai_core import (
    BindHost,
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
            content="Hello",
            usage=TokenUsage(),
        )
