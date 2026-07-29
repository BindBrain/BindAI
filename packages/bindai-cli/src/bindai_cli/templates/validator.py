from __future__ import annotations

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

        errors = []

        for filename in REQUIRED_FILES:

            if not (path / filename).exists():

                errors.append(
                    f"Missing required file: {filename}"
                )

        return errors