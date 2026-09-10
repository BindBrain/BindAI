from __future__ import annotations

import os

from bindai_core import ProviderConfiguration

from .registry import ProviderRegistry


class ProviderBuilder:
    """
    Creates provider instances through the canonical
    BindAI provider registry.
    """

    @staticmethod
    def create(
        provider: str,
        configuration: ProviderConfiguration | None = None,
    ):
        if configuration is None:
            configuration = ProviderConfiguration()

        return ProviderRegistry.create(
            provider,
            configuration,
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

        configuration = ProviderConfiguration(
            **settings,
        )

        return ProviderRegistry.create(
            provider,
            configuration,
        )

    @staticmethod
    def from_env():
        provider = os.getenv(
            "BINDAI_PROVIDER",
        )

        if not provider:
            raise ValueError("BINDAI_PROVIDER is not configured.")

        configuration = ProviderConfiguration(
            api_key=os.getenv("OPENAI_API_KEY"),
            endpoint=os.getenv("BINDAI_PROVIDER_ENDPOINT"),
            organization=os.getenv("BINDAI_PROVIDER_ORGANIZATION"),
            model=os.getenv("BINDAI_MODEL"),
        )

        return ProviderRegistry.create(
            provider,
            configuration,
        )
