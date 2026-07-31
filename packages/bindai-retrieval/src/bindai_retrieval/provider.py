from __future__ import annotations

from abc import ABC, abstractmethod

from .query import RetrievalQuery
from .result import RetrievalResult


class RetrieverProvider(ABC):
    """
    Base retrieval provider.
    """

    @abstractmethod
    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult: ...
