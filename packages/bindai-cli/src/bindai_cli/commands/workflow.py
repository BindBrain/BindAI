from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from bindai_config import ProjectRuntime
from rich import print

app = typer.Typer()


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
):

    path = resolve_workflow(
        workflow,
    )

    if not path.exists():
        print(f"[red]{path} not found.[/red]")

        raise typer.Exit(1)

    subprocess.run(
        [
            sys.executable,
            str(path),
        ],
        check=True,
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
            print(f"[red]âœ— {error}[/red]")

        raise typer.Exit(1)

    print()

    print("[green]âœ“ Workflow is valid.[/green]")


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