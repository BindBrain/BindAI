from __future__ import annotations

from .registry import ModelRegistry


class Model:

    def __init__(
        self,
        provider: str,
    ):

        self.provider = ModelRegistry.provider(
            provider,
        )()

    def generate(
        self,
        prompt: str,
        **kwargs,
    ):
        return self.provider.generate(
            prompt,
            **kwargs,
        )