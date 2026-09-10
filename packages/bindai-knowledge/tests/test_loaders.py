from pathlib import Path

from bindai_knowledge import KnowledgeDocument
from bindai_knowledge.loaders.directory_loader import DirectoryLoader
from bindai_knowledge.loaders.markdown_loader import MarkdownLoader
from bindai_knowledge.loaders.text_loader import TextLoader


def test_text_loader():
    path = Path("packages/bindai-knowledge/tests/sample.txt")
    path.write_text(
        "TEXTLOADER42 hello world",
        encoding="utf-8",
    )

    documents = TextLoader(str(path)).load()

    assert len(documents) == 1

    document = documents[0]

    assert isinstance(document, KnowledgeDocument)
    assert document.id == "sample"
    assert document.title == "sample.txt"
    assert document.content == "TEXTLOADER42 hello world"
    assert document.metadata["path"] == str(path)
    assert document.metadata["extension"] == ".txt"


def test_markdown_loader():
    path = Path("packages/bindai-knowledge/tests/sample.md")
    path.write_text(
        "# Markdown Test\n\nMARKDOWNLOADER42",
        encoding="utf-8",
    )

    documents = MarkdownLoader(str(path)).load()

    assert len(documents) == 1

    document = documents[0]

    assert document.id == "sample"
    assert document.title == "sample.md"
    assert "MARKDOWNLOADER42" in document.content
    assert document.metadata["extension"] == ".md"


def test_directory_loader_loads_txt_and_md():
    root = Path("packages/bindai-knowledge/tests/loader-fixtures")
    root.mkdir(parents=True, exist_ok=True)

    (root / "one.txt").write_text(
        "DIRECTORYTXT42",
        encoding="utf-8",
    )

    (root / "two.md").write_text(
        "# Two\n\nDIRECTORYMD42",
        encoding="utf-8",
    )

    (root / "ignored.json").write_text(
        '{"ignored": true}',
        encoding="utf-8",
    )

    documents = DirectoryLoader(str(root)).load()

    assert len(documents) == 2

    contents = {document.content for document in documents}

    assert "DIRECTORYTXT42" in contents
    assert "# Two\n\nDIRECTORYMD42" in contents


def test_directory_loader_recursive():
    root = Path("packages/bindai-knowledge/tests/loader-fixtures-recursive")
    nested = root / "nested"

    nested.mkdir(parents=True, exist_ok=True)

    (root / "root.txt").write_text(
        "ROOTLOADER42",
        encoding="utf-8",
    )

    (nested / "nested.txt").write_text(
        "NESTEDLOADER42",
        encoding="utf-8",
    )

    documents = DirectoryLoader(
        str(root),
        recursive=True,
    ).load()

    contents = {document.content for document in documents}

    assert "ROOTLOADER42" in contents
    assert "NESTEDLOADER42" in contents


def test_directory_loader_non_recursive():
    root = Path("packages/bindai-knowledge/tests/loader-fixtures-nonrecursive")
    nested = root / "nested"

    nested.mkdir(parents=True, exist_ok=True)

    (root / "root.txt").write_text(
        "ROOTONLY42",
        encoding="utf-8",
    )

    (nested / "nested.txt").write_text(
        "NESTEDONLY42",
        encoding="utf-8",
    )

    documents = DirectoryLoader(
        str(root),
        recursive=False,
    ).load()

    contents = {document.content for document in documents}

    assert "ROOTONLY42" in contents
    assert "NESTEDONLY42" not in contents
