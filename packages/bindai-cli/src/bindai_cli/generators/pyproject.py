from pathlib import Path


def generate_pyproject(
    root: Path,
    name: str,
):
    content = f"""
[project]
name = "{name.lower()}"
version = "0.1.0"
description = "{name}"
requires-python = ">=3.11"

dependencies = [
    "bindai",
]
""".strip()

    (root / "pyproject.toml").write_text(
        content,
        encoding="utf-8",
    )