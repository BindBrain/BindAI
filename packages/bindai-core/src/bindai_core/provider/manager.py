from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.model.provider import ModelProvider

from .exceptions import (
    DefaultProviderNotConfigured,
)
from .registry import ProviderRegistry

class ProviderManager:

    def __init__(self):

        self.registry = ProviderRegistry()

        self._default = None

    def register(
        self,
        provider: "ModelProvider",
        *,
        default=False,
    ):

        self.registry.register(
            provider,
        )

        if default or self._default is None:

            self._default = provider.name

    def get(
        self,
        name: str,
    ):

        return self.registry.get(
            name,
        )

    def default(
        self,
    ):

        if self._default is None:

            raise DefaultProviderNotConfigured()

        return self.registry.get(
            self._default,
        )

    def names(
        self,
    ):

        return self.registry.names()