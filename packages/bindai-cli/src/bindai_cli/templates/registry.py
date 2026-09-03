from __future__ import annotations

import json
from pathlib import Path

from .models import Template


class TemplateRegistry:
    def __init__(self):
        self.root = Path(__file__).resolve().parent
        self.scaffolds_root = self.root.parent / "scaffolds"

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
                metadata.read_text(
                    encoding="utf-8",
                )
            )

            scaffold_name = self._scaffold_name(data["name"])
            scaffold_path = self.scaffolds_root / scaffold_name

            template_data = {
                key: value
                for key, value in data.items()
                if key != "scaffold"
            }

            templates.append(
                Template(
                    **template_data,
                    path=str(scaffold_path),
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

    def _scaffold_name(self, template_name: str) -> str:
        mapping = {
            "workflow-basic": "basic",
        }

        return mapping.get(
            template_name,
            template_name,
        )
