from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StreamChunk:
    """
    Single streamed token/chunk.
    """

    delta: str = ""

    finished: bool = False