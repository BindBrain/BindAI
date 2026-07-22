from pathlib import Path

from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    TextLoader,
)


def test_text_loader(tmp_path: Path):

    file = tmp_path / "notes.txt"

    file.write_text(
        "BindAI Framework",
        encoding="utf-8",
    )

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    count = knowledge.load(
        TextLoader(
            str(file),
        )
    )

    assert count == 1

    result = knowledge.search(
        "BindAI",
    )

    assert result.success
    assert len(result.value) == 1
