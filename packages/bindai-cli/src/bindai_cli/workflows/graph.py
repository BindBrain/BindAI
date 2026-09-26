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

        nodes: list[tuple[str, str]] = []

        if ".start_node()" in source:
            nodes.append(
                ("start", "Start"),
            )

        agent_matches = re.findall(
            r"\.agent\(\s*([A-Za-z_][A-Za-z0-9_]*)",
            source,
        )

        for agent in agent_matches:
            nodes.append(
                (
                    agent,
                    f"Agent: {agent}",
                )
            )

        if ".end_node()" in source:
            nodes.append(
                ("end", "End"),
            )

        mermaid = [
            "graph TD",
        ]

        for index, (node_id, label) in enumerate(nodes):
            mermaid.append(
                f'    N{index}["{label}"]'
            )

            if index:
                mermaid.append(
                    f"    N{index - 1} --> N{index}"
                )

        return "\n".join(
            mermaid,
        )