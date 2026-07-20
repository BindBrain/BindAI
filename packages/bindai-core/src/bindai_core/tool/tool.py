from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .definition import ToolDefinition
from .result import ToolResult
from .inspector import ToolInspector


class Tool(ABC):
    """
    Base class for every BindAI tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        return ""

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:

        return ToolInspector.parameters(
            self.execute,
        )

        schema = {}

        for name, parameter in signature.parameters.items():

            if name == "self":
                continue

            annotation = parameter.annotation

            parameter_type = "string"

            if annotation is int:
                parameter_type = "integer"

            elif annotation is float:
                parameter_type = "number"

            elif annotation is bool:
                parameter_type = "boolean"

            elif annotation is list:
                parameter_type = "array"

            elif annotation is dict:
                parameter_type = "object"

            schema[name] = {

                "type": parameter_type,

                "required": (
                    parameter.default
                    is inspect.Parameter.empty
                ),

            }

        return schema

    @property
    def definition(
        self,
    ) -> ToolDefinition:

        return ToolDefinition(

            name=self.name,

            description=self.description,

            parameters=self.parameters,

        )

    @abstractmethod
    def execute(
        self,
        **kwargs,
    ) -> ToolResult:
        ...