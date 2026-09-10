from bindai_core import ProviderFactory

from .provider import OpenAIProvider


def register():
    ProviderFactory.register(
        "openai",
        OpenAIProvider,
    )


__all__ = [
    "OpenAIProvider",
    "register",
]
