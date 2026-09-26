from pathlib import Path

WORKFLOW_TEMPLATE = """from bindai_workflow import WorkflowBuilder


workflow = (
    WorkflowBuilder("{name}")
    .start_node()
    .end_node()
    .build()
)


result = workflow.run()

print(result)
"""


def generate_workflow(
    root: Path,
    name: str,
) -> None:
    workflows_dir = root / "workflows"
    workflows_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        name
        .replace(" ", "_")
        .replace("-", "_")
        .lower()
    )

    workflow_file = workflows_dir / f"{filename}.py"

    if workflow_file.exists():
        raise FileExistsError(
            f"Workflow '{name}' already exists."
        )

    workflow_file.write_text(
        WORKFLOW_TEMPLATE.format(
            name=name,
        ),
        encoding="utf-8",
    )