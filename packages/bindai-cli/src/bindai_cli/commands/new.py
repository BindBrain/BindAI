import os
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

from bindai_cli.utils.scaffold import copy_scaffold

console = Console()


def _venv_python(root: Path) -> Path:
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    return root / ".venv" / bin_dir / "python"


def _activation_command() -> str:
    if os.name == "nt":
        return ".venv\\Scripts\\activate"
    return "source .venv/bin/activate"


def new(
    name: str,
    install: bool = typer.Option(
        False,
        "--install",
        help="Install dependencies.",
    ),
) -> None:
    """
    Create a new BindAI project.
    """

    root = Path(name)

    if root.exists():
        console.print(f"[red]Project '{name}' already exists.[/red]")
        raise typer.Exit(1)

    scaffold = Path(__file__).parent.parent / "scaffolds" / "basic"

    copy_scaffold(
        scaffold,
        root,
    )

    console.print("[cyan]Creating virtual environment...[/cyan]")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(root / ".venv"),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        console.print(
            "[red]Failed to create the virtual environment.[/red]"
        )
        console.print(
            f"Project '{name}' was created, but setup is incomplete."
        )
        console.print(f"Command exited with status {exc.returncode}.")
        raise typer.Exit(1) from exc

    print()

    if install:
        console.print("[cyan]Installing dependencies...[/cyan]")

        try:
            subprocess.run(
                [
                    str(_venv_python(root)),
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(root / "requirements.txt"),
                ],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            console.print(
                "[red]Failed to install project dependencies.[/red]"
            )
            console.print(
                f"Project '{name}' was created, but setup is incomplete."
            )
            console.print(f"Command exited with status {exc.returncode}.")
            raise typer.Exit(1) from exc

        print()

    console.print(
        f"[green]✓ Project '{name}' created successfully.[/green]"
    )

    print()

    console.print("[bold]Next steps:[/bold]")

    console.print(f"  cd {name}")
    console.print(f"  {_activation_command()}")

    if not install:
        console.print("  pip install -r requirements.txt")

    console.print("  bindai doctor")
    console.print("  python main.py")