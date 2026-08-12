from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    InMemoryKnowledgeProvider,
    RecursiveChunker,
)


class FakeLoader:
    def __init__(self, documents):
        self.documents = documents

    def load(self):
        return self.documents


def test_load_without_chunker():
    provider = InMemoryKnowledgeProvider()
    knowledge = Knowledge(provider)

    documents = [
        KnowledgeDocument(
            id="doc-1",
            title="First",
            content="FIRSTLOAD42",
        ),
        KnowledgeDocument(
            id="doc-2",
            title="Second",
            content="SECONDLOAD42",
        ),
    ]

    loader = FakeLoader(documents)

    count = knowledge.load(loader)

    assert count == 2
    assert len(provider._documents) == 2

    assert provider.get("doc-1").value.content == "FIRSTLOAD42"
    assert provider.get("doc-2").value.content == "SECONDLOAD42"


def test_load_with_chunker():
    provider = InMemoryKnowledgeProvider()
    knowledge = Knowledge(provider)

    document = KnowledgeDocument(
        id="chunk-doc",
        title="Chunk Document",
        content=(
            "First paragraph with CHUNKLOAD42.\n\n"
            "Second paragraph with CHUNKLOAD43.\n\n"
            "Third paragraph with CHUNKLOAD44."
        ),
        metadata={
            "source": "test",
        },
    )

    loader = FakeLoader([document])

    count = knowledge.load(
        loader,
        chunker=RecursiveChunker(
            chunk_size=60,
            overlap=10,
        ),
    )

    assert count > 1

    chunks = list(provider._documents.values())

    assert all(
        chunk.metadata["document_id"] == "chunk-doc"
        for chunk in chunks
    )

    assert all(
        chunk.metadata["chunk"] is True
        for chunk in chunks
    )

    assert all(
        chunk.metadata["source"] == "test"
        for chunk in chunks
    )

    assert all(
        chunk.id.startswith("chunk-doc:")
        for chunk in chunks
    )


def test_load_with_chunker_preserves_title():
    provider = InMemoryKnowledgeProvider()
    knowledge = Knowledge(provider)

    document = KnowledgeDocument(
        id="title-doc",
        title="Important Document",
        content=(
            "AAAAA\n\n"
            "BBBBB\n\n"
            "CCCCC"
        ),
    )

    loader = FakeLoader([document])

    knowledge.load(
        loader,
        chunker=RecursiveChunker(
            chunk_size=8,
            overlap=2,
        ),
    )

    chunks = list(provider._documents.values())

    assert len(chunks) == 3

    assert all(
        chunk.title == "Important Document"
        for chunk in chunks
    )


def test_load_returns_zero_for_empty_loader():
    provider = InMemoryKnowledgeProvider()
    knowledge = Knowledge(provider)

    loader = FakeLoader([])

    count = knowledge.load(loader)

    assert count == 0
    assert len(provider._documents) == 0


def test_load_without_chunker_preserves_metadata():
    provider = InMemoryKnowledgeProvider()
    knowledge = Knowledge(provider)

    document = KnowledgeDocument(
        id="metadata-doc",
        title="Metadata",
        content="METADATA42",
        metadata={
            "environment": "test",
            "version": 2,
        },
    )

    loader = FakeLoader([document])

    knowledge.load(loader)

    stored = provider.get("metadata-doc").value

    assert stored.metadata == {
        "environment": "test",
        "version": 2,
    }