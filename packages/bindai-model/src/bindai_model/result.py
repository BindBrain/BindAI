from dataclasses import dataclass


@dataclass(slots=True)
class ModelResult:

    content: str

    model: str

    provider: str

    finish_reason: str | None = None

    usage: dict | None = None