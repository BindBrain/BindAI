from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class RequestStep(ABC):
    @abstractmethod
    def process(
        self,
        agent,
        context,
        request,
    ): ...
