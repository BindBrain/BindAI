from __future__ import annotations

import re
from pathlib import Path


class WorkflowGraph:
    @staticmethod
    def generate(
        path: Path,
    ) -> str:

        source = path.read_text(
            encoding="utf-8",
        )

        nodes = re.findall(
            r'\.step\(\s*"([^"]+)"',
            source,
        )

        mermaid = [
            "graph TD",
        ]

        for i, node in enumerate(nodes):
            mermaid.append(f'    N{i}["{node}"]')

            if i:
                mermaid.append(f"    N{i - 1} --> N{i}")

        return "\n".join(
            mermaid,
        )
