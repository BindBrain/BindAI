from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
)

from .provider import OpenAIProvider
from bindai_providers import ProviderRegistry

from .provider import OpenAIProvider

def register():

    ProviderRegistry.register(
        "openai",
        lambda configuration: OpenAIProvider(
            configuration,
        ),
    )


__all__ = [
    "OpenAIProvider",
    "register",
]
