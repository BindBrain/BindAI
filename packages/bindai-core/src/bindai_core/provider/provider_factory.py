from __future__ import annotations

from bindai_core.model import ModelProvider

from .configuration import ProviderConfiguration


class ProviderFactory:
    """
    Creates model providers from registered provider types.
    """

    _providers: dict[type[ModelProvider], type[ModelProvider]] = {}

    @classmethod
    def register(
        cls,
        provider: type[ModelProvider],
    ) -> None:
        cls._providers[provider] = provider

    @classmethod
    def create(
        cls,
        provider: type[ModelProvider],
        configuration: ProviderConfiguration | None = None,
    ) -> ModelProvider:

        if provider not in cls._providers:
            raise ValueError(
                f"Provider '{provider.__name__}' is not registered."
            )

        return cls._providers[provider](configuration)