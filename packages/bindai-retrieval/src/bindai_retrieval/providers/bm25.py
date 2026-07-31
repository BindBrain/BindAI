from __future__ import annotations

from ..provider import RetrieverProvider
from ..query import RetrievalQuery
from ..result import RetrievalResult


class BM25RetrieverProvider(RetrieverProvider):
    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:

        raise NotImplementedError
