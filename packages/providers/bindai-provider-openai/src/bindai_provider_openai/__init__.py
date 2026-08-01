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
