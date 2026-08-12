from bindai_knowledge import (
    EmbeddingProvider,
    KnowledgeDocument,
    VectorKnowledgeProvider,
)


class ControlledEmbeddingProvider:
    def __init__(self, vectors: dict[str, list[float]]):
        self.vectors = vectors

    def embed(self, text: str) -> list[float]:
        return self.vectors[text]


def document(
    document_id: str,
    content: str,
) -> KnowledgeDocument:
    return KnowledgeDocument(
        id=document_id,
        title=document_id,
        content=content,
    )


def test_vector_search_uses_cosine_similarity():
    embedding = ControlledEmbeddingProvider(
        {
            "query": [1.0, 0.0],
            "first": [1.0, 0.0],
            "second": [0.0, 1.0],
        }
    )

    provider = VectorKnowledgeProvider(embedding)

    provider.add_many(
        [
            document("first", "first"),
            document("second", "second"),
        ]
    )

    result = provider.search_with_scores(
        "query",
        limit=2,
    )

    assert result.success

    first_score, first_document = result.value[0]
    second_score, second_document = result.value[1]

    assert first_document.id == "first"
    assert second_document.id == "second"

    assert first_score == 1.0
    assert second_score == 0.0


def test_vector_search_respects_limit():
    embedding = ControlledEmbeddingProvider(
        {
            "query": [1.0, 0.0],
            "one": [1.0, 0.0],
            "two": [0.9, 0.1],
            "three": [0.0, 1.0],
        }
    )

    provider = VectorKnowledgeProvider(embedding)

    provider.add_many(
        [
            document("one", "one"),
            document("two", "two"),
            document("three", "three"),
        ]
    )

    result = provider.search(
        "query",
        limit=2,
    )

    assert result.success
    assert len(result.value) == 2

    assert [item.id for item in result.value] == [
        "one",
        "two",
    ]


def test_hybrid_search_combines_keyword_and_vector_candidates():
    embedding = ControlledEmbeddingProvider(
        {
            "query": [1.0, 0.0],
            "query query query query": [0.0, 1.0],
            "unrelated text": [1.0, 0.0],
        }
    )

    provider = VectorKnowledgeProvider(embedding)

    provider.add_many(
        [
            document(
                "keyword-match",
                "query query query query",
            ),
            document(
                "vector-match",
                "unrelated text",
            ),
        ]
    )

    result = provider.hybrid_search(
        "query",
        limit=2,
    )

    assert result.success
    assert len(result.value) == 2

    ids = [item.id for item in result.value]

    assert "keyword-match" in ids
    assert "vector-match" in ids

def test_hybrid_search_normalizes_keyword_and_vector_scores():
    embedding = ControlledEmbeddingProvider(
        {
            "query": [1.0, 0.0],
            "query query query query query": [0.0, 1.0],
            "unrelated": [1.0, 0.0],
        }
    )

    provider = VectorKnowledgeProvider(embedding)

    provider.add_many(
        [
            document(
                "keyword-only",
                "query query query query query",
            ),
            document(
                "vector-only",
                "unrelated",
            ),
            document(
                "balanced",
                "query",
            ),
        ]
    )

    result = provider.hybrid_search(
        "query",
        limit=3,
    )

    assert result.success

    ids = [item.id for item in result.value]

    assert ids == [
        "balanced",
        "keyword-only",
        "vector-only",
    ]