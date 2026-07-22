from pathlib import Path

from bindai_knowledge import (
    JsonKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


def test_json_provider_persistence(tmp_path: Path):

    db = tmp_path / "knowledge.json"

    knowledge = Knowledge(
        JsonKnowledgeProvider(db),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="Python",
            content="Python is awesome.",
        )
    )

    knowledge = Knowledge(
        JsonKnowledgeProvider(db),
    )

    result = knowledge.search("Python")

    assert result.success
    assert len(result.value) == 1
    assert result.value[0].title == "Python"
