from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.provider.configuration import ProviderConfiguration

from .embedding import EmbeddingResponse
from .provider_capabilities import ProviderCapabilities
from .request import ModelRequest
from .response import ModelResponse
from .stream_chunk import StreamChunk


class ModelProvider(ABC):
    """
    Base class for every model provider.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique provider name.
        Example:
            "openai"
            "anthropic"
            "ollama"
        """
        ...

    def __init__(
        self,
        configuration: ProviderConfiguration | None = None,
    ):
        self.configuration = configuration or ProviderConfiguration()

    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        """
        Default provider capabilities.

        Providers override when needed.
        """

        return ProviderCapabilities()

    @abstractmethod
    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """
        Generate a complete response.
        """
        ...

    def stream(
        self,
        request: ModelRequest,
    ):
        """
        Default streaming implementation.

        Providers supporting true streaming
        should override this.
        """

        response = self.generate(
            request,
        )

        yield StreamChunk(
            delta=response.content,
            finished=True,
        )

    def embed(
        self,
        text: str,
    ) -> EmbeddingResponse:
        """
        Embedding API.

        Providers without embeddings
        should override or raise.
        """

        raise NotImplementedError("Embeddings not supported.")
