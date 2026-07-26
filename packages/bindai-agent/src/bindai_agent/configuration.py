from dataclasses import dataclass


@dataclass(slots=True)
class AgentConfiguration:
    temperature: float | None = None

    max_tokens: int | None = None

    max_tool_iterations: int = 10

    stream: bool = False

    verbose: bool = False
