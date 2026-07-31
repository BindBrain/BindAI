from __future__ import annotations

import importlib.util
from pathlib import Path
from bindai_tool import Tool

class ToolLoader:
    @staticmethod
    def load(
        root: Path,
    ) -> list:

        tools: list[object] = []

        folder = root / "tools"

        if not folder.exists():
            return tools

        for file in folder.glob("*.py"):
            if file.name.startswith("_"):
                continue

            spec = importlib.util.spec_from_file_location(
                file.stem,
                file,
            )

            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            for value in vars(module).values():
                if (
                    hasattr(value, "function")
                    and hasattr(value, "name")
                    and hasattr(value, "description")
                ):
                    tools.append(value)

        return tools
