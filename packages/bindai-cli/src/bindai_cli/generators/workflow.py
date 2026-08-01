from pathlib import Path

WORKFLOW_TEMPLATE = """from bindai_workflow import WorkflowBuilder


workflow = (
    WorkflowBuilder()
    .name("{name}")
    .build()
)
"""


def generate_workflow(
    root: Path,
    name: str,
) -> None:
    workflows_dir = root / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    filename = name.replace(" ", "_").replace("-", "_").lower()

    workflow_file = workflows_dir / f"{filename}.py"

    if workflow_file.exists():
        raise FileExistsError(f"Workflow '{name}' already exists.")

    workflow_file.write_text(
        WORKFLOW_TEMPLATE.format(name=name),
        encoding="utf-8",
    )
