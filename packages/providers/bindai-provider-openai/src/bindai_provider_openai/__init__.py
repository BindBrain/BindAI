from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
)

from .provider import OpenAIProvider


def register():

    ProviderRegistry.register(
        "openai",
        lambda **kwargs: OpenAIProvider(
            ProviderConfiguration(
                **kwargs,
            )
        ),
    )


__all__ = [
    "OpenAIProvider",
    "register",
]
