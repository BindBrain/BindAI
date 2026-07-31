from __future__ import annotations

import shutil
from pathlib import Path

from .registry import TemplateRegistry
from .validator import TemplateValidator


class TemplateInstaller:
    def __init__(self):

        self.registry = TemplateRegistry()

    def install(
        self,
        name: str,
        destination: Path,
    ):

        template = self.registry.get(name)

        if template is None:
            raise ValueError(f"Unknown template '{name}'.")

        source = Path(template.path)

        errors = TemplateValidator.validate(source)

        if errors:
            raise ValueError("\n".join(errors))

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                ".pytest_cache",
                "*.pyc",
                ".env",
            ),
        )

        example = destination / ".env.example"

        env = destination / ".env"

        if example.exists() and not env.exists():
            shutil.copy2(
                example,
                env,
            )

        errors = TemplateValidator.validate(source)

        if errors:
            raise ValueError("\n".join(errors))
