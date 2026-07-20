from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AgentConfiguration:
    """
    Configuration describing how an agent behaves.

    This class contains only configuration.
    No execution logic belongs here.
    """

    #
    # Identity
    #

    name: str = ""

    description: str = ""

    instructions: str = ""

    #
    # Model
    #

    model: str | None = None

    temperature: float = 0.7

    top_p: float = 1.0

    max_tokens: int | None = None

    #
    # Generation
    #

    stream: bool = False

    response_format: str | None = None

    stop_sequences: list[str] = field(
        default_factory=list,
    )

    #
    # Tool execution
    #

    tool_choice: str = "auto"

    max_tool_iterations: int = 10

    #
    # Memory
    #

    memory_enabled: bool = True

    #
    # Runtime
    #

    timeout: int | None = None

    #
    # Metadata
    #

    tags: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
