from __future__ import annotations

from bindai_core.embeddings import EmbeddingProvider


class Embedding:
    def __init__(
        self,
        provider: EmbeddingProvider,
    ):
        self.provider = provider

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed(
            text,
        )
