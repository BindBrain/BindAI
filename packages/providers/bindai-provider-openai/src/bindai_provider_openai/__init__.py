from bindai_core.provider import ProviderConfiguration
from bindai_providers import ProviderRegistry

from .client import OpenAIClient
from .mapper import OpenAIMapper
from .provider import OpenAIProvider


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
    "OpenAIClient",
    "OpenAIMapper",
]