from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.model.request import ModelRequest
    from bindai_core.model.response import ModelResponse


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        ...

    @abstractmethod
    def stream(
        self,
        request: ModelRequest,
    ):
        ...

    @property
    @abstractmethod
    def capabilities(self):
        ...