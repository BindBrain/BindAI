from bindai_model import ModelRegistry
from bindai_model.provider import ModelProvider


class DummyProvider(ModelProvider):

    def generate(
        self,
        prompt,
        **kwargs,
    ):
        return prompt


def test_registry():

    ModelRegistry.register(
        "dummy",
        DummyProvider,
    )

    provider = ModelRegistry.provider(
        "dummy",
    )()

    assert provider.generate("hello") == "hello"