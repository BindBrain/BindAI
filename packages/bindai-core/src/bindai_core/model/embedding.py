from dataclasses import dataclass


@dataclass(slots=True)
class EmbeddingResponse:
    """
    Response returned by embedding models.
    """

    embedding: list[float]

    model: str