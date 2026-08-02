from __future__ import annotations

from bindai_core.embeddings import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed(
        self,
        text: str,
    ) -> list[float]:

        text = text.lower()

        return [
            float(sum(ord(c) for c in text)),
            float(len(text)),
        ]
