from __future__ import annotations

from pathlib import Path


class ProjectInspector:
    def __init__(
        self,
        root: Path,
    ):
        self.root = root

    def inspect(self) -> dict:

        return {
            "agents": self._files("agents"),
            "tools": self._files("tools"),
            "workflows": self._files("workflows"),
            "knowledge": self._files("knowledge"),
            "memory": self._files("memory"),
            "templates": self._files("templates"),
        }

    def _files(
        self,
        folder: str,
    ) -> list[str]:

        path = self.root / folder

        if not path.exists():
            return []

        return sorted(file.stem for file in path.glob("*.py") if file.name != "__init__.py")
