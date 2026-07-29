from __future__ import annotations

import shutil
from pathlib import Path


def copy_scaffold(
    scaffold: Path,
    destination: Path,
) -> None:

    shutil.copytree(
        scaffold,
        destination,
    )

    replace_placeholders(
        destination,
        destination.name,
    )


def replace_placeholders(
    root: Path,
    project_name: str,
):

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix not in {
            ".py",
            ".toml",
            ".md",
            ".txt",
            ".example",
        }:
            continue

        text = file.read_text(
            encoding="utf-8",
        )

        text = text.replace(
            "{{PROJECT_NAME}}",
            project_name,
        )

        file.write_text(
            text,
            encoding="utf-8",
        )