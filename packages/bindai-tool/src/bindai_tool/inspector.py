from __future__ import annotations

import inspect

from typing import Any
from typing import Callable


class ToolInspector:
    """
    Inspects Python callables and produces
    provider-agnostic tool metadata.
    """

    @staticmethod
    def parameters(
        function: Callable[..., Any],
    ) -> dict[str, Any]:

        signature = inspect.signature(
            function,
        )

        schema = {}

        for name, parameter in signature.parameters.items():
            if name == "self":
                continue

            annotation = parameter.annotation

            parameter_type = ToolInspector._python_type(
                annotation,
            )

            schema[name] = {
                "type": parameter_type,
                "required": (parameter.default is inspect.Parameter.empty),
            }

        return schema

    @staticmethod
    def _python_type(
        annotation,
    ) -> str:

        if annotation is int:
            return "integer"

        if annotation is float:
            return "number"

        if annotation is bool:
            return "boolean"

        if annotation is list:
            return "array"

        if annotation is dict:
            return "object"

        return "string"
