from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


def test_search_with_scores():

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

    result = knowledge.search_with_scores(
        "python",
    )

    assert result.success
    assert len(result.value) == 1

    score, document = result.value[0]

    assert score > 0
    assert document.title == "Python"
