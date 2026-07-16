from __future__ import annotations

import inspect
from abc import ABC
from abc import abstractmethod
from typing import Any

from .definition import ToolDefinition
from .result import ToolResult


class Tool(ABC):
    """
    Base class for every BindAI tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique tool name.
        """
        ...

    @property
    def description(self) -> str:
        """
        Human-readable description.
        """
        return ""

    @property
    def parameters(self) -> dict[str, Any]:
        """
        Automatically generate a parameter schema
        from the execute() method.
        """

        signature = inspect.signature(self.execute)

        schema: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():

            if name == "self":
                continue

            annotation = parameter.annotation

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
            else:
                parameter_type = "string"

            schema[name] = {
                "type": parameter_type,
                "required": parameter.default is inspect.Parameter.empty,
            }

        return schema

    def definition(self) -> ToolDefinition:
        """
        Returns a provider-agnostic tool definition.
        """

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
        """
        Execute the tool.
        """
        ...