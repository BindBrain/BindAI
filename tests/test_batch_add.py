from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


def test_add_many():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    result = knowledge.add_many(
        [
            KnowledgeDocument(
                id="1",
                title="Python",
                content="Python",
            ),
            KnowledgeDocument(
                id="2",
                title="Java",
                content="Java",
            ),
        ]
    )

    assert result.success

    search = knowledge.search("python")

    assert search.success
    assert len(search.value) == 1
    assert search.value[0].title == "Python"