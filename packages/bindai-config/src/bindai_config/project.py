from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProjectConfig:
    name: str = "BindAI Project"

    provider: str = "openai"

    model: str = "gpt-4.1-mini"

    temperature: float = 0.7

    timeout: int = 60

    entrypoint: str = "main.py"

    memory: str = "memory"

    knowledge: str = "knowledge"

    templates: str = "templates"

    workflows: str = "workflows"

    agents: str = "agents"

    tools: str = "tools"
