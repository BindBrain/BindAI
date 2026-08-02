from __future__ import annotations

from typing import Protocol


class EmbeddingProvider(Protocol):
    """
    Interface for embedding generation providers.
    """

    def embed(
        self,
        text: str,
    ) -> list[float]: ...
