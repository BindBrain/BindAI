from pathlib import Path

from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    MarkdownLoader,
)


def test_markdown_loader(tmp_path: Path):

    file = tmp_path / "readme.md"

    file.write_text(
        "# BindAI\n\nFramework",
        encoding="utf-8",
    )

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    count = knowledge.load(
        MarkdownLoader(str(file))
    )

    assert count == 1

    result = knowledge.search("BindAI")

    assert result.success
    assert len(result.value) == 1