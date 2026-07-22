from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
    StreamChunk,
)


class ProviderClient(ABC):
    """
    Base class for provider-specific SDK clients.

    Responsible only for communicating with
    external AI providers.
    """

    @abstractmethod
    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse: ...

    @abstractmethod
    def stream(
        self,
        request: ModelRequest,
    ):
        yield StreamChunk(
            delta="",
            finished=True,
        )
