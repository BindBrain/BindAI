from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FILES = {
    "README.md",
    "main.py",
}


class TemplateValidator:
    @staticmethod
    def validate(
        path: Path,
    ) -> list[str]:

        errors: list[str] = []

        # Required files
        for filename in REQUIRED_FILES:
            if not (path / filename).exists():
                errors.append(f"Missing required file: {filename}")

        # Stop early if template.json doesn't exist
        metadata = path / "template.json"

        if not metadata.exists():
            return errors

        # Validate metadata structure
        try:
            data = json.loads(
                metadata.read_text(
                    encoding="utf-8",
                )
            )

        except Exception:
            errors.append("Invalid template.json")

            return errors

        required_fields = [
            "name",
            "version",
            "category",
            "description",
        ]

        for field in required_fields:
            if field not in data:
                errors.append(f"template.json missing '{field}'.")

        return errors
