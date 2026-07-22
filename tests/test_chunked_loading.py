from pathlib import Path

from bindai_knowledge import (
    FixedChunker,
    InMemoryKnowledgeProvider,
    Knowledge,
    TextLoader,
)


def test_chunked_loading(tmp_path: Path):

    file = tmp_path / "notes.txt"

    file.write_text(
        "abcdefghij",
        encoding="utf-8",
    )

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    count = knowledge.load(
        TextLoader(str(file)),
        chunker=FixedChunker(
            chunk_size=4,
            overlap=1,
        ),
    )

    assert count == 4
