from dataclasses import dataclass


@dataclass(slots=True)
class StreamChunk:
    """
    Represents a streamed model response chunk.
    """

    delta: str

    finished: bool = False