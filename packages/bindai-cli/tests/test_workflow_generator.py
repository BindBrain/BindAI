from pathlib import Path

from bindai_cli.generators.workflow import generate_workflow


def test_generate_workflow_creates_valid_builder_skeleton(
    tmp_path: Path,
):
    generate_workflow(
        tmp_path,
        "Research Workflow",
    )

    workflow_file = (
        tmp_path
        / "workflows"
        / "research_workflow.py"
    )

    assert workflow_file.exists()

    source = workflow_file.read_text(
        encoding="utf-8",
    )

    assert 'WorkflowBuilder("Research Workflow")' in source
    assert ".start_node()" in source
    assert ".end_node()" in source
    assert ".build()" in source
    assert ".run()" in source
    assert "print(result)" in source
    assert ".name(" not in source