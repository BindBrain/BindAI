from bindai_providers import ProviderRegistry


def test_provider_registry():

    class DummyProvider:

        def __init__(
            self,
            value,
        ):
            self.value = value

    ProviderRegistry.register(
        "dummy",
        lambda value: DummyProvider(value),
    )

    provider = ProviderRegistry.create(
        "dummy",
        value=123,
    )

    assert provider.value == 123