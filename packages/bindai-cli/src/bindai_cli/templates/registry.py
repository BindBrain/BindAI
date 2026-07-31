from __future__ import annotations

import json
from pathlib import Path

from .models import Template


class TemplateRegistry:
    def __init__(self):

        current = Path(__file__).resolve()

        while current.name != "bindai":
            current = current.parent

        self.root = current / "templates"

    def list(self) -> list[Template]:

        templates = []

        for folder in sorted(self.root.iterdir()):
            metadata = folder / "template.json"

            if not metadata.exists():
                continue

            data = json.loads(metadata.read_text(encoding="utf-8"))

            templates.append(
                Template(
                    **data,
                    path=str(folder),
                )
            )

        return templates

    # <-- ADD THIS METHOD HERE

    def get(
        self,
        name: str,
    ) -> Template | None:

        for template in self.list():
            if template.name == name:
                return template

        return None
