from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import typer
from bindai_config import ProjectRuntime
from rich import print
from typer.core import TyperGroup


class WorkflowGroup(TyperGroup):
    def resolve_command(
        self,
        ctx,
        args,
    ):
        if args and args[0] not in self.commands:
            workflow_name = args[0]

            runtime = ProjectRuntime(
                Path.cwd(),
            )

            workflows_dir = (
                Path.cwd()
                / runtime.config.workflows
            )

            workflow_file = (
                workflow_name
                .replace("-", "_")
                .replace(" ", "_")
                .lower()
            )

            candidates = [
                workflows_dir / f"{workflow_file}.py",
                workflows_dir / f"{workflow_file}_workflow.py",
            ]

            path = next(
                (
                    candidate
                    for candidate in candidates
                    if candidate.exists()
                ),
                None,
            )

            if path is not None:
                return (
                    "run",
                    self.commands["run"],
                    [
                        str(path),
                        *args[1:],
                    ],
                )

        return super().resolve_command(
            ctx,
            args,
        )


app = typer.Typer(
    cls=WorkflowGroup,
)


def resolve_workflow(
    workflow: str | None,
) -> Path:

    runtime = ProjectRuntime(
        Path.cwd(),
    )

    if workflow is None:
        workflow = runtime.config.entrypoint

    return Path(workflow)


@app.command("run")
def run(
    workflow: str = typer.Argument(
        ...,
        help="Workflow entrypoint.",
    ),
    args: list[str] = typer.Argument(
        None,
        help="Arguments passed to the workflow entrypoint.",
    ),
):

    project_root = Path.cwd()
    path = resolve_workflow(
        workflow,
    )

    if not path.exists():
        print(f"[red]{path} not found.[/red]")

        raise typer.Exit(1)

    environment = os.environ.copy()

    existing_pythonpath = environment.get("PYTHONPATH")
    if existing_pythonpath:
        environment["PYTHONPATH"] = (
            f"{project_root}{os.pathsep}{existing_pythonpath}"
        )
    else:
        environment["PYTHONPATH"] = str(project_root)

    subprocess.run(
        [
            sys.executable,
            str(path),
            *args,
        ],
        check=True,
        env=environment,
    )


@app.command("validate")
def validate(
    workflow: str | None = typer.Argument(
        None,
    ),
):

    from bindai_cli.workflows.validator import (
        WorkflowValidator,
    )

    path = resolve_workflow(
        workflow,
    )

    errors = WorkflowValidator.validate(
        path,
    )

    if errors:
        print()

        for error in errors:
            print(
                f"[red]✓ {error}[/red]"
            )

        raise typer.Exit(1)

    print()

    print(
        "[green]✓ Workflow is valid.[/green]"
    )


@app.command("graph")
def graph(
    workflow: str | None = typer.Argument(
        None,
    ),
):

    from bindai_cli.workflows.graph import (
        WorkflowGraph,
    )

    path = resolve_workflow(
        workflow,
    )

    if not path.exists():
        print(f"[red]{path} not found.[/red]")

        raise typer.Exit(1)

    print()

    print(
        WorkflowGraph.generate(
            path,
        )
    )