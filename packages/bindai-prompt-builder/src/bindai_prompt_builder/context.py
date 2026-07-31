from __future__ import annotations

from dataclasses import dataclass

from bindai_core.model import ModelRequest


@dataclass(slots=True)
class PromptBuildContext:
    request: ModelRequest

    tools: list

    output_type: type | None = None
