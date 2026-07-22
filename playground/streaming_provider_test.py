from bindai_core import (
    ModelProvider,
    ModelResponse,
    ModelRequest,
    TokenUsage,
)


class DummyProvider(ModelProvider):
    @property
    def name(self):
        return "dummy"

    def generate(self, request):

        return ModelResponse(
            content="Hello BindAI!",
            usage=TokenUsage(),
        )


provider = DummyProvider()

for chunk in provider.stream(ModelRequest()):
    print(chunk.delta, chunk.finished)
