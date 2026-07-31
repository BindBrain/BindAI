from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.model.request import ModelRequest
    from bindai_core.model.response import ModelResponse
    from bindai_core.provider.configuration import ProviderConfiguration


class ModelProvider(ABC):
    """
    Base provider interface.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        self.configuration = configuration

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse: ...

    @abstractmethod
    def stream(
        self,
        request: ModelRequest,
    ): ...

    @property
    @abstractmethod
    def capabilities(self): ...
