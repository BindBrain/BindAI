from bindai_knowledge import KnowledgeDocument
from bindai_retrieval import RetrievalQuery
from bindai_retrieval.providers.hybrid import HybridRetrieverProvider


def test_hybrid_retriever():
    documents = [
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python programming language",
        ),
        KnowledgeDocument(
            id="2",
            title="Java",
            content="Enterprise programming language",
        ),
    ]

    provider = HybridRetrieverProvider(
        documents,
    )

    result = provider.retrieve(
        RetrievalQuery(
            text="python",
        )
    )

    assert result.success
    assert result.documents
    assert result.documents[0].id == "1"


def test_hybrid_retriever_combines_results():
    documents = [
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python programming language",
        ),
        KnowledgeDocument(
            id="2",
            title="Software Development",
            content="Building applications with modern programming tools.",
        ),
    ]

    provider = HybridRetrieverProvider(
        documents,
    )

    result = provider.retrieve(
        RetrievalQuery(
            text="building applications",
            limit=2,
        )
    )

    assert result.success
    assert len(result.documents) == 2
    assert result.documents[0].id == "2"