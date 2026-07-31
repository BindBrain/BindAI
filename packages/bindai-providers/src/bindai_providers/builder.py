from __future__ import annotations

import os

from .registry import ProviderRegistry


class ProviderBuilder:
    """
    Creates provider instances.
    """

    @staticmethod
    def create(
        provider: str,
        **kwargs,
    ):
        return ProviderRegistry.create(
            provider,
            **kwargs,
        )

    @staticmethod
    def from_config(
        config: dict,
    ):
        provider = config["provider"]

        settings = config.get(
            "settings",
            {},
        )

        return ProviderRegistry.create(
            provider,
            **settings,
        )

    @staticmethod
    def from_env():
        provider = os.getenv(
            "BINDAI_PROVIDER",
        )

        if not provider:
            raise ValueError(
                "BINDAI_PROVIDER is not configured."
            )

        return ProviderRegistry.create(
            provider,
        )