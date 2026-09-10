from __future__ import annotations

from openai import OpenAI

from .provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI embedding provider.
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        dimensions: int = 512,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self.dimensions = dimensions

        self.client = OpenAI(
            api_key=api_key,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )

        return response.data[0].embedding
