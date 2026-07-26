from __future__ import annotations

from pathlib import Path
import yaml

from .builder import AgentBuilder


class AgentLoader:

    @staticmethod
    def from_yaml(path: str | Path):

        with open(path, "r", encoding="utf8") as f:
            config = yaml.safe_load(f)

        builder = AgentBuilder()

        if "model" in config:
            builder.model(config["model"])

        if "instructions" in config:
            builder.instructions(
                config["instructions"],
            )

        return builder.build()