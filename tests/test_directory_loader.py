from pathlib import Path

from bindai_knowledge import (
    DirectoryLoader,
)


def test_directory_loader(tmp_path: Path):

    (tmp_path / "a.txt").write_text(
        "Alpha",
        encoding="utf-8",
    )

    (tmp_path / "b.txt").write_text(
        "Beta",
        encoding="utf-8",
    )

    loader = DirectoryLoader(
        str(tmp_path),
    )

    documents = loader.load()

    assert len(documents) == 2

    titles = {d.title for d in documents}

    assert "a.txt" in titles

    assert "b.txt" in titles
