from __future__ import annotations

from bindai_core.model import ModelProvider


class ProviderFactory:

    _providers: dict[
        str,
        type[ModelProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[ModelProvider],
    ):

        cls._providers[
            name.lower()
        ] = provider

    @classmethod
    def create(
        cls,
        name: str,
        configuration=None,
    ):

        provider = cls._providers.get(
            name.lower(),
        )

        if provider is None:

            raise ValueError(
                f"Unknown provider '{name}'."
            )

        return provider(
            configuration,
        )

    @classmethod
    def names(
        cls,
    ):

        return tuple(
            sorted(
                cls._providers.keys(),
            )
        )