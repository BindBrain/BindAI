from bindai_core import (
    ProviderFactory,
    ModelProvider,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):
    def __init__(self):
        pass

    @property
    def name(self):
        return "dummy"

    def generate(self, request):
        return ModelResponse(
            content="Hello from DummyProvider",
            usage=TokenUsage(),
        )


ProviderFactory.register(
    "dummy",
    DummyProvider,
)

provider = ProviderFactory.create("dummy")

print(provider.name)
print(ProviderFactory.names())
