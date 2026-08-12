from bindai_knowledge import (
    FakeEmbeddingProvider,
    Knowledge,
    KnowledgeDocument,
    VectorKnowledgeProvider,
)


def make_document(
    document_id: str,
    content: str,
    metadata: dict | None = None,
) -> KnowledgeDocument:
    return KnowledgeDocument(
        id=document_id,
        title=document_id,
        content=content,
        metadata=metadata or {},
    )


def test_add_creates_vector_record():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    document = make_document(
        "doc-1",
        "Python programming",
    )

    result = provider.add(document)

    assert result.success
    assert result.value == document

    assert "doc-1" in provider._vectors

    record = provider._vectors["doc-1"]

    assert record.document == document
    assert record.embedding == [
        float(sum(ord(c) for c in "python programming")),
        float(len("python programming")),
    ]


def test_add_many_creates_documents_and_vectors():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    documents = [
        make_document("doc-1", "Python"),
        make_document("doc-2", "JavaScript"),
    ]

    result = provider.add_many(documents)

    assert result.success
    assert result.value == documents

    assert set(provider._documents) == {
        "doc-1",
        "doc-2",
    }

    assert set(provider._vectors) == {
        "doc-1",
        "doc-2",
    }


def test_search_returns_documents_ranked_by_vector_similarity():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    documents = [
        make_document("python", "Python programming"),
        make_document("cats", "Cats and animals"),
        make_document("python-2", "Python development"),
    ]

    provider.add_many(documents)

    result = provider.search(
        "Python programming",
        limit=2,
    )

    assert result.success
    assert result.value

    assert len(result.value) == 2
    assert result.value[0].id == "python"


def test_search_respects_limit():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add_many(
        [
            make_document("one", "one"),
            make_document("two", "two"),
            make_document("three", "three"),
        ]
    )

    result = provider.search(
        "one",
        limit=1,
    )

    assert result.success
    assert len(result.value) == 1


def test_search_with_scores_returns_scores():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    document = make_document(
        "doc-1",
        "Python programming",
    )

    provider.add(document)

    result = provider.search_with_scores(
        "Python programming",
        limit=1,
    )

    assert result.success
    assert len(result.value) == 1

    score, returned_document = result.value[0]

    assert returned_document == document
    assert score > 0.99


def test_metadata_filter_is_applied_to_vector_search():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add_many(
        [
            make_document(
                "python",
                "Python programming",
                {"language": "python"},
            ),
            make_document(
                "javascript",
                "Python programming",
                {"language": "javascript"},
            ),
        ]
    )

    result = provider.search(
        "Python programming",
        filters={"language": "python"},
    )

    assert result.success
    assert [document.id for document in result.value] == [
        "python",
    ]


def test_delete_removes_document_and_vector():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add(
        make_document(
            "doc-1",
            "Python",
        )
    )

    assert "doc-1" in provider._documents
    assert "doc-1" in provider._vectors

    result = provider.delete("doc-1")

    assert result.success
    assert "doc-1" not in provider._documents
    assert "doc-1" not in provider._vectors


def test_clear_removes_documents_and_vectors():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add_many(
        [
            make_document("doc-1", "Python"),
            make_document("doc-2", "JavaScript"),
        ]
    )

    result = provider.clear()

    assert result.success
    assert provider._documents == {}
    assert provider._vectors == {}


def test_hybrid_search_returns_results():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add_many(
        [
            make_document("python", "Python programming"),
            make_document("javascript", "JavaScript programming"),
            make_document("database", "Database systems"),
        ]
    )

    result = provider.hybrid_search(
        "Python programming",
        limit=2,
    )

    assert result.success
    assert len(result.value) == 2
    assert result.value[0].id == "python"


def test_hybrid_search_respects_metadata_filter():
    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    provider.add_many(
        [
            make_document(
                "python",
                "Python programming",
                {"type": "language"},
            ),
            make_document(
                "database",
                "Python database",
                {"type": "database"},
            ),
        ]
    )

    result = provider.hybrid_search(
        "Python",
        limit=5,
        filters={"type": "language"},
    )

    assert result.success
    assert [document.id for document in result.value] == [
        "python",
    ]