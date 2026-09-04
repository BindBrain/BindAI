from bindai_core import ProviderFactory

from .provider import GroqProvider


def register():
    ProviderFactory.register("groq", GroqProvider)


__all__ = ["GroqProvider", "register"]
