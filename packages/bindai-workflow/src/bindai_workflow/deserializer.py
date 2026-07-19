from __future__ import annotations

import json

from pathlib import Path

from .factory import WorkflowFactory


class WorkflowDeserializer:
    """
    Loads workflows from JSON.
    """

    def __init__(
        self,
        factory: WorkflowFactory,
    ):

        self.factory = factory

    def from_json(
        self,
        data: str,
    ):

        return self.factory.create(

            json.loads(
                data,
            )

        )

    def load(
        self,
        path: str |Path,
    ):

        return self.from_json(

            Path(path).read_text(

                encoding="utf8",

            )

        )