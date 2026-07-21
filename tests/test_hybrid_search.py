from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    VectorKnowledgeProvider,
)
from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    VectorKnowledgeProvider,
    FakeEmbeddingProvider,
)


def test_hybrid_search():

    provider = VectorKnowledgeProvider(
        FakeEmbeddingProvider(),
    )

    knowledge = Knowledge(provider)

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
            title="Java",
            content="Enterprise programming language",
        )
    )

    result = provider.hybrid_search(
        "python",
    )

    assert result.success
    assert result.value
    assert result.value[0].title == "Python"