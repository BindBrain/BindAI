from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentDefinition:
    """Declarative definition of a BindAI agent."""

    id: str
    name: str
    provider: str | None = None
    model: str | None = None
    connection: str | None = None
    instructions: str = ""
    temperature: float | None = None
    max_tokens: int | None = None
    max_tool_iterations: int = 10
    stream: bool = False
    verbose: bool = False

    tools: list[str] = field(default_factory=list)
    memory: str | None = None
    retriever: str | None = None
    knowledge: str | None = None
    middleware: list[str] = field(default_factory=list)
    hooks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentDefinition:
        if not isinstance(data, dict):
            raise TypeError("Agent definition must be a mapping.")

        required = {"id", "name"}
        missing = required - data.keys()
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"Missing required agent fields: {names}.")

        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            provider=data.get("provider"),
            model=data.get("model"),
            connection=data.get("connection"),
            instructions=str(data.get("instructions", "")),
            temperature=data.get("temperature"),
            max_tokens=data.get("max_tokens"),
            max_tool_iterations=int(data.get("max_tool_iterations", 10)),
            stream=bool(data.get("stream", False)),
            verbose=bool(data.get("verbose", False)),
            tools=[str(value) for value in data.get("tools", [])],
            memory=data.get("memory"),
            retriever=data.get("retriever"),
            knowledge=data.get("knowledge"),
            middleware=[str(value) for value in data.get("middleware", [])],
            hooks=[str(value) for value in data.get("hooks", [])],
        )
