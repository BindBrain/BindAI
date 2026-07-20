from bindai_knowledge import (
    DummyEmbeddingProvider,
    Knowledge,
    KnowledgeDocument,
    VectorKnowledgeProvider,
)


def test_vector_provider_returns_documents():

    knowledge = Knowledge(
        VectorKnowledgeProvider(
            DummyEmbeddingProvider(),
        )
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python programming language",
        )
    )

    knowledge.add(
        KnowledgeDocument(
            id="2",
            title="Cats",
            content="Cats are animals",
        )
    )

    result = knowledge.search(
        "python",
    )

    assert result.success
    assert len(result.value) == 2