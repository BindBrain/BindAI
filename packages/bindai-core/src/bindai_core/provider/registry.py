from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model_provider import ModelProvider

from .exceptions import (
    ProviderAlreadyRegistered,
    ProviderNotFound,
)


class ProviderRegistry:
    def __init__(self):

        self._providers: dict[
            str,
            "ModelProvider",
        ] = {}

    def register(
        self,
        provider: "ModelProvider",
    ):

        if provider.name in self._providers:
            raise ProviderAlreadyRegistered(
                provider.name,
            )

        self._providers[provider.name] = provider

    def get(
        self,
        name: str,
    ) -> "ModelProvider":

        if name not in self._providers:
            raise ProviderNotFound(
                name,
            )

        return self._providers[name]

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._providers

    def remove(
        self,
        name: str,
    ):

        self._providers.pop(
            name,
            None,
        )

    def clear(
        self,
    ):

        self._providers.clear()

    def names(
        self,
    ):

        return tuple(
            self._providers.keys(),
        )

    def all(
        self,
    ):

        return tuple(
            self._providers.values(),
        )

    def __len__(
        self,
    ):

        return len(
            self._providers,
        )
