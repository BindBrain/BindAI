from bindai_core import ProviderFactory

from .provider import OpenRouterProvider


def register():
    ProviderFactory.register("openrouter", OpenRouterProvider)


__all__ = ["OpenRouterProvider", "register"]
