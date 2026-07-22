from dataclasses import dataclass


@dataclass(slots=True)
class AgentConfiguration:
    temperature: float = 0.7

    max_tokens: int | None = None

    max_tool_iterations: int = 10

    stream: bool = False

    verbose: bool = False
