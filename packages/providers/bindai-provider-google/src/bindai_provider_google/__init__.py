from bindai_core import ProviderFactory

from .provider import GoogleProvider


def register():
    ProviderFactory.register("google", GoogleProvider)


__all__ = ["GoogleProvider", "register"]
