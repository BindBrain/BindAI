from __future__ import annotations

import json


class OutputParser:

    @staticmethod
    def parse(
        text: str,
        output_type,
    ):

        if output_type is None:
            return text

        data = json.loads(
            text,
        )

        return output_type(
            **data,
        )