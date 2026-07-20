from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    InMemoryKnowledgeProvider,
)


def test_add_document():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    document = KnowledgeDocument(
        id="1",
        title="Python",
        content="Python is a programming language.",
    )

    result = knowledge.add(
        document,
    )

    assert result.success

    stored = knowledge.get(
        "1",
    )

    assert stored.success
    assert stored.value.title == "Python"


def test_search_documents():

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

    knowledge.add(
        KnowledgeDocument(
            id="2",
            title="Docker",
            content="Container platform",
        )
    )

    result = knowledge.search(
        "python",
    )

    assert result.success
    assert len(result.value) == 1
    assert result.value[0].id == "1"


def test_delete_document():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Programming language",
        )
    )

    knowledge.delete(
        "1",
    )

    result = knowledge.get(
        "1",
    )

    assert result.success
    assert result.value is None


def test_clear_documents():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Programming",
        )
    )

    knowledge.add(
        KnowledgeDocument(
            id="2",
            title="Docker",
            content="Containers",
        )
    )

    knowledge.clear()

    result = knowledge.search(
        "",
    )

    assert result.success
    assert len(result.value) == 0