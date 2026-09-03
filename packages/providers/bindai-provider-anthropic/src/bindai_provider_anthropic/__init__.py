from bindai_core import ProviderFactory

from .provider import AnthropicProvider


def register():
    ProviderFactory.register("anthropic", AnthropicProvider)


__all__ = ["AnthropicProvider", "register"]
