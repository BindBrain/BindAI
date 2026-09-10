from bindai_knowledge import KnowledgeDocument, RecursiveChunker


def test_empty_document_returns_no_chunks():
    document = KnowledgeDocument(
        id="empty",
        title="Empty",
        content="",
    )

    chunks = RecursiveChunker(chunk_size=100, overlap=20).chunk(document)

    assert chunks == []


def test_small_document_returns_one_chunk():
    document = KnowledgeDocument(
        id="small",
        title="Small",
        content="This is a small document.",
    )

    chunks = RecursiveChunker(chunk_size=100, overlap=20).chunk(document)

    assert len(chunks) == 1
    assert chunks[0].id == "small:0"
    assert chunks[0].document_id == "small"
    assert chunks[0].content == "This is a small document."


def test_chunk_ids_are_deterministic():
    document = KnowledgeDocument(
        id="doc",
        title="Document",
        content="First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
    )

    chunks = RecursiveChunker(chunk_size=25, overlap=5).chunk(document)

    assert [chunk.id for chunk in chunks] == [
        "doc:0",
        "doc:1",
        "doc:2",
    ]


def test_document_metadata_is_preserved():
    document = KnowledgeDocument(
        id="metadata",
        title="Metadata",
        content="Metadata should survive chunking.",
        metadata={
            "source": "test",
            "version": 1,
        },
    )

    chunks = RecursiveChunker(chunk_size=100, overlap=20).chunk(document)

    assert len(chunks) == 1
    assert chunks[0].metadata == document.metadata


def test_document_id_is_preserved():
    document = KnowledgeDocument(
        id="source-document",
        title="Source",
        content="Some content.",
    )

    chunks = RecursiveChunker(chunk_size=100, overlap=20).chunk(document)

    assert all(chunk.document_id == "source-document" for chunk in chunks)


def test_chunks_do_not_exceed_chunk_size():
    document = KnowledgeDocument(
        id="size",
        title="Size",
        content=(
            "Paragraph one contains enough text to create a chunk.\n\n"
            "Paragraph two also contains enough text to create another chunk."
        ),
    )

    chunk_size = 50

    chunks = RecursiveChunker(
        chunk_size=chunk_size,
        overlap=10,
    ).chunk(document)

    assert chunks

    assert all(len(chunk.content) <= chunk_size for chunk in chunks)


def test_large_paragraph_is_split():
    document = KnowledgeDocument(
        id="large",
        title="Large",
        content="A" * 250,
    )

    chunks = RecursiveChunker(
        chunk_size=100,
        overlap=20,
    ).chunk(document)

    assert len(chunks) > 1

    assert all(len(chunk.content) <= 100 for chunk in chunks)


def test_overlap_is_present_between_adjacent_chunks():
    document = KnowledgeDocument(
        id="overlap",
        title="Overlap",
        content="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )

    chunks = RecursiveChunker(
        chunk_size=10,
        overlap=3,
    ).chunk(document)

    assert len(chunks) > 1

    for previous, current in zip(chunks, chunks[1:]):
        assert previous.content[-3:] == current.content[:3]
