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


def test_knowledge_search_can_rerank_results():
    from bindai_knowledge import (
        InMemoryKnowledgeProvider,
        Knowledge,
    )

    knowledge = Knowledge(InMemoryKnowledgeProvider())

    knowledge.add_many(
        [
            KnowledgeDocument(
                id="1",
                title="Python",
                content="Python programming language.",
            ),
            KnowledgeDocument(
                id="2",
                title="AI Agents",
                content="AI agents use tools.",
            ),
        ]
    )

    reranker = LexicalReranker()

    result = knowledge.search(
        "AI agents tools",
        limit=2,
        reranker=reranker,
    )

    assert result.success
    assert result.value[0].id == "2"


def test_knowledge_retrieve_with_sources_includes_citations():
    from bindai_knowledge import (
        InMemoryKnowledgeProvider,
        Knowledge,
    )

    knowledge = Knowledge(InMemoryKnowledgeProvider())

    knowledge.add(
        KnowledgeDocument(
            id="doc-1",
            title="AI Guide",
            content="AI agents can use tools.",
        )
    )

    sources = knowledge.retrieve_with_sources(
        "AI agents",
        limit=1,
    )

    assert len(sources) == 1
    assert sources[0]["citation"] == "[1]"
    assert sources[0]["id"] == "doc-1"
    assert sources[0]["title"] == "AI Guide"
