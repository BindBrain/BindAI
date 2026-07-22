from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
    KnowledgeSearchOptions,
)


def test_search_options():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python programming language",
        )
    )

    options = KnowledgeSearchOptions(
        limit=1,
    )

    result = knowledge.search(
        "Python",
        options=options,
    )

    assert result.success
    assert len(result.value) == 1
