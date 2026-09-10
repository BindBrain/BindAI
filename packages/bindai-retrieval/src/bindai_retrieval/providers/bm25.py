from __future__ import annotations

import math
import re
from collections import Counter

from bindai_knowledge import KnowledgeDocument

from ..provider import RetrieverProvider
from ..query import RetrievalQuery
from ..result import RetrievalResult


class BM25RetrieverProvider(RetrieverProvider):
    def __init__(
        self,
        documents: list[KnowledgeDocument],
    ):
        self.documents = documents

        self._tokenized_documents = [
            self._tokenize(
                self._document_text(document),
            )
            for document in documents
        ]

        self._document_frequencies: Counter[str] = Counter()

        for tokens in self._tokenized_documents:
            for token in set(tokens):
                self._document_frequencies[token] += 1

        self._average_document_length = (
            sum(len(tokens) for tokens in self._tokenized_documents)
            / len(self._tokenized_documents)
            if self._tokenized_documents
            else 0.0
        )

    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:

        scored = self.score_documents(
            query,
        )

        return RetrievalResult(
            success=True,
            documents=[document for _, document in scored[: query.limit]],
        )

    def score_documents(
        self,
        query: RetrievalQuery,
    ) -> list[tuple[float, KnowledgeDocument]]:

        query_tokens = self._tokenize(
            query.text,
        )

        if not query_tokens:
            return []

        document_count = len(self.documents)

        if document_count == 0:
            return []

        scored: list[tuple[float, KnowledgeDocument]] = []

        for document, tokens in zip(
            self.documents,
            self._tokenized_documents,
        ):
            if query.metadata:
                if not all(
                    document.metadata.get(key) == value for key, value in query.metadata.items()
                ):
                    continue

            score = self._score(
                query_tokens,
                tokens,
                document_count,
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        document,
                    )
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return scored

    def _score(
        self,
        query_tokens: list[str],
        document_tokens: list[str],
        document_count: int,
    ) -> float:

        if not document_tokens:
            return 0.0

        k1 = 1.5
        b = 0.75

        document_length = len(document_tokens)

        length_normalization = (
            1 - b + b * (document_length / self._average_document_length)
            if self._average_document_length
            else 1.0
        )

        frequencies = Counter(
            document_tokens,
        )

        score = 0.0

        for token in query_tokens:
            term_frequency = frequencies.get(
                token,
                0,
            )

            if term_frequency == 0:
                continue

            document_frequency = self._document_frequencies.get(
                token,
                0,
            )

            idf = math.log(
                1 + (document_count - document_frequency + 0.5) / (document_frequency + 0.5)
            )

            score += (
                idf * (term_frequency * (k1 + 1)) / (term_frequency + k1 * length_normalization)
            )

        return score

    @staticmethod
    def _document_text(
        document: KnowledgeDocument,
    ) -> str:

        return f"{document.title} {document.content}"

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:

        return re.findall(
            r"\b\w+\b",
            text.lower(),
        )
