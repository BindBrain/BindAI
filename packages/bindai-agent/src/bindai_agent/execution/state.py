from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)


@dataclass(slots=True)
class ExecutionState:
    """
    Shared mutable state for the
    execution pipeline.
    """

    #
    # Model
    #

    request: ModelRequest | None = None

    response: ModelResponse | None = None

    #
    # Runtime
    #

    iterations: int = 0

    finished: bool = False

    cancelled: bool = False

    streaming: bool = False

    #
    # Scratchpad
    #

    metadata: dict = field(
        default_factory=dict,
    )
