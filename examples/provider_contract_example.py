from bindai_core.model import (
    ModelProvider,
    ProviderCapabilities,
    ModelRequest,
    ModelResponse,
)


class DemoProvider(ModelProvider):
    @property
    def name(self):
        return "demo"

    @property
    def capabilities(self):
        return ProviderCapabilities()

    def generate(self, request):
        return ModelResponse(
            content="Hello from Demo Provider",
            model="demo-model",
        )


provider = DemoProvider()

response = provider.generate(ModelRequest())

print(provider.name)
print(provider.capabilities.chat)
print(response.content)
