from __future__ import annotations

from bindai_core.model import ModelProvider


class ProviderFactory:
    """
    Creates provider instances.
    """

    _providers: dict[str, type[ModelProvider]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider_type: type[ModelProvider],
    ):

        cls._providers[name.lower()] = provider_type

    @classmethod
    def create(
        cls,
        name: str,
        **kwargs,
    ) -> ModelProvider:

        provider = cls._providers.get(name.lower())

        if provider is None:
            raise ValueError(
                f"Unknown provider '{name}'."
            )

        return provider(**kwargs)

    @classmethod
    def names(cls):

        return sorted(cls._providers.keys())