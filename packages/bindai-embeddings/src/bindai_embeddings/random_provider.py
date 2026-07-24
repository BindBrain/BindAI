from __future__ import annotations

import hashlib

from .provider import EmbeddingProvider


class RandomEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic bag-of-words embeddings.

    Used only for tests.
    """

    DIMENSION = 128

    def embed(
        self,
        text: str,
    ) -> list[float]:

        vector = [0.0] * self.DIMENSION

        #
        # tokenize
        #

        for token in text.lower().split():

            index = (
                int(
                    hashlib.sha256(
                        token.encode(),
                    ).hexdigest(),
                    16,
                )
                % self.DIMENSION
            )

            vector[index] += 1.0

        #
        # normalize
        #

        norm = sum(v * v for v in vector) ** 0.5

        if norm > 0:

            vector = [
                v / norm
                for v in vector
            ]

        return vector