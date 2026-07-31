from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from bindai_cli.templates.installer import TemplateInstaller
from bindai_cli.templates.registry import TemplateRegistry
from bindai_cli.templates.validator import TemplateValidator

app = typer.Typer()

console = Console()


@app.command("list")
def list_templates():

    registry = TemplateRegistry()

    table = Table(title="Available Templates")

    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Description")

    for template in registry.list():
        table.add_row(
            template.name,
            template.category,
            template.status,
            template.description,
        )

    console.print(table)


@app.command("install")
def install_template(
    name: str,
):

    console.print("[cyan]Installing template...[/cyan]")

    installer = TemplateInstaller()

    console.print(" • Reading metadata")

    console.print(" • Copying files")

    destination = Path.cwd()

    if any(destination.iterdir()):
        console.print("[yellow]Current directory is not empty.[/yellow]")
        raise typer.Exit(1)

    installer.install(
        name,
        destination,
    )

    console.print(" • Creating environment")

    console.print()

    console.print(f"[green]✓ Template '{name}' installed successfully.[/green]")


@app.command("create")
def create_template(
    template: str,
    project: str,
):
    """
    Create a new project from a template.
    """

    from bindai_cli.utils.scaffold import copy_scaffold

    registry = TemplateRegistry()

    template_obj = registry.get(template)

    if template_obj is None:
        console.print(f"[red]Unknown template:[/red] {template}")

        raise typer.Exit(1)

    destination = Path(project)

    if destination.exists():
        console.print(f"[red]Project '{project}' already exists.[/red]")

        raise typer.Exit(1)

    copy_scaffold(
        Path(template_obj.path),
        destination,
    )

    console.print()

    console.print(f"[green]✓ Created project '{project}' from template '{template}'.[/green]")

    console.print()

    console.print("[bold]Next steps:[/bold]")

    console.print(f"  cd {project}")

    console.print("  .venv\\Scripts\\activate")

    console.print("  pip install -r requirements.txt")

    console.print("  python main.py")


@app.command("info")
def info_template(
    name: str,
):

    registry = TemplateRegistry()

    template = registry.get(name)

    if template is None:
        console.print(f"[red]Unknown template:[/red] {name}")
        raise typer.Exit(1)

    table = Table(title=template.title)

    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Name", template.name)
    table.add_row("Version", template.version)
    table.add_row("Author", template.author)
    table.add_row("Category", template.category)
    table.add_row("Status", template.status)
    table.add_row("Description", template.description)
    table.add_row(
        "Tags",
        ", ".join(template.tags),
    )

    console.print(table)


@app.command("search")
def search_templates(
    query: str,
):

    registry = TemplateRegistry()

    templates = registry.list()

    query = query.lower()

    matches = [
        template
        for template in templates
        if (
            query in template.name.lower()
            or query in template.title.lower()
            or query in template.description.lower()
            or query in template.category.lower()
            or any(query in tag.lower() for tag in template.tags)
        )
    ]

    if not matches:
        console.print(f"[yellow]No templates found for '{query}'.[/yellow]")
        raise typer.Exit()

    table = Table(title=f"Search: {query}")

    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Description")

    for template in matches:
        table.add_row(
            template.name,
            template.category,
            template.status,
            template.description,
        )

    console.print(table)


@app.command("validate")
def validate_template(
    name: str,
):

    registry = TemplateRegistry()

    template = registry.get(name)

    if template is None:
        console.print("[red]Template not found.[/red]")

        raise typer.Exit(1)

    errors = TemplateValidator.validate(Path(template.path))

    if not errors:
        console.print("[green]✓ Template is valid.[/green]")

        return

    console.print("[red]Template has problems:[/red]")

    for error in errors:
        console.print(f" • {error}")
