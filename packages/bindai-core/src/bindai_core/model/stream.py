from dataclasses import dataclass


@dataclass(slots=True)
class StreamChunk:
    """
    A single streamed response chunk.
    """

    content: str

    finished: bool = False