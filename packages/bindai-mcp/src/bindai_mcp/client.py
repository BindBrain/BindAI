from __future__ import annotations

import httpx
from bindai_tool import Tool
from bindai_tool.definition import ToolDefinition
from bindai_tool.result import ToolResult


class MCPTool(Tool):
    def __init__(
        self,
        client,
        name: str,
        description: str,
        schema: dict | None = None,
    ):
        self.client = client
        self._name = name
        self._description = description
        self.schema = schema or {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def definition(self):

        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.schema,
        )

    def execute(
        self,
        context,
    ):

        arguments = {}

        if hasattr(context, "variables"):
            arguments = context.variables

        response = httpx.post(
            f"{self.client.url}/call",
            json={
                "tool": self.name,
                "arguments": arguments,
            },
        )

        response.raise_for_status()

        return ToolResult(
            success=True,
            output=response.json(),
        )


class MCPClient:
    def __init__(
        self,
        url: str,
    ):
        self.url = url

    async def list_tools(self):

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.url}/tools")

            response.raise_for_status()

            data = response.json()

        return [
            MCPTool(
                client=self,
                name=item["name"],
                description=item.get(
                    "description",
                    "",
                ),
                schema=item.get(
                    "schema",
                    {},
                ),
            )
            for item in data
        ]
