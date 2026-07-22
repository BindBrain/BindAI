from bindai_knowledge import (
    FixedChunker,
    KnowledgeDocument,
)


def test_fixed_chunker_creates_chunks():

    document = KnowledgeDocument(
        id="1",
        title="Test",
        content="abcdefghij",
    )

    chunker = FixedChunker(
        chunk_size=4,
        overlap=1,
    )

    chunks = chunker.chunk(
        document,
    )

    assert len(chunks) == 4

    assert chunks[0].content == "abcd"

    assert chunks[1].content == "defg"

    assert chunks[0].document_id == "1"
