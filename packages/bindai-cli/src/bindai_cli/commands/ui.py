from __future__ import annotations

from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

console = Console()

app = typer.Typer(
    invoke_without_command=True,
)


def _workspace_projects(root: Path):
    from bindai_project import ProjectStudioService

    if (root / "bindai.toml").is_file():
        return ProjectStudioService.discover_projects(root.parent)

    return ProjectStudioService.discover_projects(root)


def _configure_projects(root: Path) -> int:
    from bindai_api.routes.studio import configure_studio_workspace

    workspace_root = (
        root.parent
        if (root / "bindai.toml").is_file()
        else root
    )

    projects = _workspace_projects(root)
    configure_studio_workspace(workspace_root)

    return len(projects)


@app.callback()
def ui(
    port: int = typer.Option(
        8000,
        "--port",
        help="Local Studio server port.",
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Local Studio server host.",
    ),
) -> None:
    """
    Start the local BindAI Studio server.
    """
    load_dotenv(override=True)
    root = Path.cwd().resolve()

    if not (root / "bindai.toml").is_file():
        projects = _workspace_projects(root)

        if not projects:
            console.print(
                "[yellow]No BindAI projects found in the current directory.[/yellow]"
            )
            console.print()
            console.print("Create a project first with:")
            console.print("  bindai new <name>")
            raise typer.Exit(1)

    try:
        import uvicorn
    except ImportError as exc:
        console.print(
            "[red]BindAI Studio dependencies are not installed.[/red]"
        )
        console.print()
        console.print("Install them with:")
        console.print('  pip install "bindai-cli[studio]"')
        raise typer.Exit(1) from exc

    # Configure Studio before importing the API application.
    project_count = _configure_projects(root)

    try:
        from bindai_api.app import app as studio_app
    except ImportError as exc:
        console.print(
            "[red]BindAI Studio dependencies are not installed.[/red]"
        )
        console.print()
        console.print('Install them with: pip install "bindai-cli[studio]"')
        raise typer.Exit(1) from exc

    console.print(
        f"[green]BindAI Studio[/green] - {project_count} project(s) discovered"
    )
    console.print(
        f"Starting server at http://{host}:{port}"
    )
    console.print("Press Ctrl+C to stop.")

    uvicorn.run(
        studio_app,
        host=host,
        port=port,
    )
