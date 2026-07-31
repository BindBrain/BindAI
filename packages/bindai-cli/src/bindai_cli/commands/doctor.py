from __future__ import annotations

import os
import platform
import sys

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from bindai_cli.utils.config import load_config
from bindai_cli.utils.providers import installed_providers

load_dotenv()

app = typer.Typer(
    invoke_without_command=True,
)

console = Console()


@app.callback()
def doctor() -> None:
    """
    Check BindAI installation and project configuration.
    """

    table = Table(title="BindAI Doctor")

    table.add_column("Check", style="cyan")
    table.add_column("Status")

    #
    # Python
    #

    table.add_row(
        "Python",
        f"✅ {platform.python_version()}",
    )

    #
    # Virtual Environment
    #

    venv = hasattr(sys, "real_prefix") or sys.prefix != sys.base_prefix

    table.add_row(
        "Virtual Environment",
        "✅ Active" if venv else "❌ Not Active",
    )

    #
    # Configuration
    #

    config = load_config()

    if config:
        table.add_row("Project", config.name)

        table.add_row("Default Provider", config.provider)

        table.add_row("Default Model", config.model)
    else:
        table.add_row(
            "Configuration",
            "⚠ No bindai.toml",
        )

    #
    # Templates
    #

    from bindai_cli.templates.registry import TemplateRegistry

    registry = TemplateRegistry()

    table.add_row(
        "Templates",
        f"✅ {len(registry.list())} available",
    )

    #
    # Installed Providers
    #

    providers = installed_providers()

    if providers:
        table.add_row(
            "Providers",
            ", ".join(providers),
        )
    else:
        table.add_row(
            "Providers",
            "⚠ None installed",
        )

    #
    # Environment Variables
    #

    table.add_row(
        "OPENAI_API_KEY",
        "✅ Configured" if os.getenv("OPENAI_API_KEY") else "⚠ Missing",
    )

    table.add_row(
        "ANTHROPIC_API_KEY",
        "✅ Configured" if os.getenv("ANTHROPIC_API_KEY") else "⚠ Missing",
    )

    table.add_row(
        "OLLAMA_HOST",
        os.getenv("OLLAMA_HOST", "localhost"),
    )

    console.print(table)
