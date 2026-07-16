from __future__ import annotations

from bindai_core.model import ModelProvider


class ProviderRegistry:
    """
    Registry of model providers.
    """

    def __init__(self):

        self._providers: dict[str, ModelProvider] = {}

    def register(
        self,
        provider: ModelProvider,
    ):

        self._providers[
            provider.name
        ] = provider

    def get(
        self,
        name: str,
    ) -> ModelProvider:

        return self._providers[name]

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._providers

    def names(
        self,
    ):

        return list(
            self._providers.keys()
        )

    def __len__(self):

        return len(
            self._providers
        )