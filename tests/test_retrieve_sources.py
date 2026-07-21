from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


def test_retrieve_with_sources():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python is great.",
            metadata={
                "language": "python",
            },
        )
    )

    results = knowledge.retrieve_with_sources(
        "python",
    )

    assert len(results) == 1
    assert results[0]["title"] == "Python"
    assert results[0]["content"] == "Python is great."
    assert results[0]["metadata"]["language"] == "python"