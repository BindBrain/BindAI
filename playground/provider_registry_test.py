from bindai_core import (
    ProviderRegistry,
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


registry = ProviderRegistry()

registry.register(
    DummyProvider(),
)

print(
    registry.names()
)

print(
    registry.contains("dummy")
)

print(
    registry.get("dummy").name
)