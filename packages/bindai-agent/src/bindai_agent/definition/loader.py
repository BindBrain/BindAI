from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import AgentDefinition


class AgentDefinitionLoader:
    """Load and save declarative BindAI agent definitions."""

    def load(self, path: str | Path) -> AgentDefinition:
        agent_path = Path(path)

        with agent_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if data is None:
            raise ValueError(f"Agent definition is empty: {agent_path}")

        return AgentDefinition.from_dict(data)

    def save(
        self,
        definition: AgentDefinition,
        path: str | Path,
    ) -> Path:
        agent_path = Path(path)
        agent_path.parent.mkdir(parents=True, exist_ok=True)

        data: dict[str, Any] = definition.to_dict()

        agent_path.write_text(
            yaml.safe_dump(
                data,
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

        return agent_path
