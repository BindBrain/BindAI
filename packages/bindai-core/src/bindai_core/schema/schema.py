from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ResponseSchema:
    """
    Provider-independent structured output schema.
    """

    model: type[Any]

    json_schema: dict
