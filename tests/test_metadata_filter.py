from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


def test_metadata_filter():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python",
            metadata={
                "language": "python",
            },
        )
    )

    knowledge.add(
        KnowledgeDocument(
            id="2",
            title="Java",
            content="Java",
            metadata={
                "language": "java",
            },
        )
    )

    result = knowledge.search(
        "python",
        filters={
            "language": "python",
        },
    )

    assert result.success
    assert len(result.value) == 1
    assert result.value[0].title == "Python"
