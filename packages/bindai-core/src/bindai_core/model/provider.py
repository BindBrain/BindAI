from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.provider.configuration import ProviderConfiguration

from .capabilities import ProviderCapabilities
from .request import ModelRequest
from .response import ModelResponse
from .stream_chunk import StreamChunk


class ModelProvider(ABC):
    """
    Base class for all LLM providers.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration | None = None,
    ):
        self.configuration = configuration or ProviderConfiguration()

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def capabilities(self) -> ProviderCapabilities:
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
        Stream model output.

        Default implementation falls back
        to generate().
        """

        response = self.generate(request)

        yield StreamChunk(
            delta=response.content,
            finished=True,
        )