from bindai_knowledge import KnowledgeDocument
from bindai_knowledge.reranker import LexicalReranker


def test_lexical_reranker_orders_by_query_overlap():
    reranker = LexicalReranker()

    documents = [
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python is a programming language.",
        ),
        KnowledgeDocument(
            id="2",
            title="AI Agents",
            content="AI agents use tools and reasoning.",
        ),
        KnowledgeDocument(
            id="3",
            title="AI",
            content="AI systems can use tools.",
        ),
    ]

    result = reranker.rerank(
        "AI agents tools",
        documents,
    )

    assert [document.id for document in result] == [
        "2",
        "3",
        "1",
    ]


def test_lexical_reranker_preserves_order_when_query_has_no_terms():
    reranker = LexicalReranker()

    documents = [
        KnowledgeDocument(
            id="1",
            title="First",
            content="First document.",
        ),
        KnowledgeDocument(
            id="2",
            title="Second",
            content="Second document.",
        ),
    ]

    result = reranker.rerank(
        "",
        documents,
    )

    assert result == documents