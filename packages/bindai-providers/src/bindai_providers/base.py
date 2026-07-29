from __future__ import annotations

from abc import ABC, abstractmethod

from .models import (
    ProviderCapabilities,
    ProviderConfiguration,
)


class ModelProvider(ABC):
    """
    Base class for all model providers.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        self.configuration = configuration

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        ...

    @abstractmethod
    def generate(
        self,
        request,
    ):
        ...

    @abstractmethod
    def stream(
        self,
        request,
    ):
        ...