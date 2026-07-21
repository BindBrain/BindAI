from bindai_knowledge import (
    KnowledgeDocument,
    RecursiveChunker,
)


def test_recursive_chunker_prefers_paragraphs():

    document = KnowledgeDocument(
        id="1",
        title="Test",
        content=(
            "Paragraph one.\n\n"
            "Paragraph two.\n\n"
            "Paragraph three."
        ),
    )

    chunker = RecursiveChunker(
        chunk_size=30,
    )

    chunks = chunker.chunk(
        document,
    )

    assert len(chunks) >= 2

    assert "Paragraph one." in chunks[0].content