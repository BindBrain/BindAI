from bindai_core import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    TokenUsage,
)

from bindai_core.provider import ProviderManager


class DummyProvider(ModelProvider):

    @property
    def name(self):
        return "dummy"

    def generate(self, request):

        return ModelResponse(
            content="Hello from Dummy Provider",
            usage=TokenUsage(),
        )


manager = ProviderManager()

manager.register(
    DummyProvider(),
    default=True,
)

provider = manager.default()

response = provider.generate(
    ModelRequest()
)

print(provider.name)
print(response.content)
print(manager.names())
print(len(manager))