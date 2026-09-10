from bindai_core import ProviderFactory

from .provider import OllamaProvider


def register():
    ProviderFactory.register("ollama", OllamaProvider)


__all__ = ["OllamaProvider", "register"]
