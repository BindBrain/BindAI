from pathlib import Path

from bindai_knowledge import (
    HTMLLoader,
    InMemoryKnowledgeProvider,
    Knowledge,
)


def test_html_loader(tmp_path: Path):

    file = tmp_path / "page.html"

    file.write_text(
        """
        <html>
            <body>
                <h1>BindAI</h1>
                <p>AI Framework</p>
            </body>
        </html>
        """,
        encoding="utf-8",
    )

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    count = knowledge.load(
        HTMLLoader(
            str(file),
        )
    )

    assert count == 1

    result = knowledge.search(
        "Framework",
    )

    assert result.success
    assert len(result.value) == 1
