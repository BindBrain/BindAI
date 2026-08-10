from __future__ import annotations

import json
from pathlib import Path

from .models import Template


class TemplateRegistry:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def list(self) -> list[Template]:
        templates: list[Template] = []

        if not self.root.exists():
            return templates

        for folder in sorted(self.root.iterdir()):
            if not folder.is_dir():
                continue

            metadata = folder / "template.json"

            if not metadata.exists():
                continue

            data = json.loads(
                metadata.read_text(encoding="utf-8")
            )

            templates.append(
                Template(
                    **data,
                    path=str(folder),
                )
            )

        return templates

    def get(
        self,
        name: str,
    ) -> Template | None:

        for template in self.list():
            if template.name == name:
                return template

        return None
