from bindai_core.model import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    TokenUsage,
)

from bindai_core.provider import (
    ProviderConfiguration,
    ProviderRegistry,
)


class FakeProvider(ModelProvider):
    @property
    def name(self):

        return "fake"

    def generate(
        self,
        request,
    ):

        return ModelResponse(
            content="ok",
            usage=TokenUsage(),
        )


def test_provider_registry():

    registry = ProviderRegistry()

    provider = FakeProvider(ProviderConfiguration())

    registry.register(provider)

    assert registry.contains("fake")

    assert registry.get("fake") is provider


def test_provider_generate():

    provider = FakeProvider(ProviderConfiguration())

    response = provider.generate(ModelRequest())

    assert response.content == "ok"
