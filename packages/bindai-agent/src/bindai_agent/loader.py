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

        #
        # Basic settings
        #

        if "name" in config:
            builder.name(
                config["name"],
            )

        if "model" in config:
            builder.model(
                config["model"],
            )

        if "instructions" in config:
            builder.instructions(
                config["instructions"],
            )

        #
        # Configuration
        #

        if "temperature" in config:
            builder.temperature(
                config["temperature"],
            )

        if "max_tokens" in config:
            builder.max_tokens(
                config["max_tokens"],
            )

        if "max_tool_iterations" in config:
            builder.max_tool_iterations(
                config["max_tool_iterations"],
            )

        return builder.build()