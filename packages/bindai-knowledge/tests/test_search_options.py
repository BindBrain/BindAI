from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
    KnowledgeSearchOptions,
)


def test_search_options_defaults():
    options = KnowledgeSearchOptions()

    assert options.limit == 5
    assert options.filters is None
    assert options.min_score == 0.0
    assert options.search_type == "keyword"


def test_search_options_can_select_vector_search():
    options = KnowledgeSearchOptions(
        limit=3,
        search_type="vector",
    )

    assert options.limit == 3
    assert options.search_type == "vector"


def test_search_options_can_select_hybrid_search():
    options = KnowledgeSearchOptions(
        limit=3,
        search_type="hybrid",
    )

    assert options.limit == 3
    assert options.search_type == "hybrid"


def test_search_options_min_score():
    options = KnowledgeSearchOptions(
        min_score=0.75,
    )

    assert options.min_score == 0.75


def test_keyword_search_remains_default():
    knowledge = Knowledge(
        InMemoryKnowledgeProvider()
    )

    knowledge.add(
        KnowledgeDocument(
            id="doc-1",
            title="Python",
            content="Python programming language.",
        )
    )

    result = knowledge.search("Python")

    assert result.success
    assert len(result.value) == 1
    assert result.value[0].id == "doc-1"

