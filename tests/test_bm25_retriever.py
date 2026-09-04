from bindai_knowledge import KnowledgeDocument
from bindai_retrieval import RetrievalQuery
from bindai_retrieval.providers.bm25 import BM25RetrieverProvider

def test_bm25_ranks_relevant_documents():
    documents = [
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python is a programming language used for building applications.",
        ),
        KnowledgeDocument(
            id="2",
            title="Programming",
            content="Programming languages are used to build software.",
        ),
    ]

    provider = BM25RetrieverProvider(documents)

    result = provider.retrieve(
        RetrievalQuery(
            text="Python programming",
            limit=2,
        )
    )

    assert result.success
    assert len(result.documents) == 2
    assert result.documents[0].id == "1"