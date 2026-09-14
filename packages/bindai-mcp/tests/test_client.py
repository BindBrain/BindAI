from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bindai_mcp import MCPClient, MCPTool


@pytest.mark.asyncio
async def test_list_tools():
    response = MagicMock()
    response.json.return_value = [
        {
            "name": "search",
            "description": "Search documents",
            "schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
            },
        }
    ]
    response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.get = AsyncMock(return_value=response)

    with patch(
        "bindai_mcp.client.httpx.AsyncClient",
        return_value=mock_client,
    ):
        tools = await MCPClient("http://localhost:8000").list_tools()

    mock_client.get.assert_awaited_once_with(
        "http://localhost:8000/tools",
    )

    response.raise_for_status.assert_called_once_with()

    assert len(tools) == 1
    assert isinstance(tools[0], MCPTool)
    assert tools[0].name == "search"
    assert tools[0].description == "Search documents"
    assert tools[0].schema["properties"]["query"]["type"] == "string"


@pytest.mark.asyncio
async def test_list_tools_uses_defaults_for_optional_fields():
    response = MagicMock()
    response.json.return_value = [
        {
            "name": "ping",
        }
    ]
    response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.get = AsyncMock(return_value=response)

    with patch(
        "bindai_mcp.client.httpx.AsyncClient",
        return_value=mock_client,
    ):
        tools = await MCPClient("http://localhost:8000").list_tools()

    assert len(tools) == 1
    assert tools[0].name == "ping"
    assert tools[0].description == ""
    assert tools[0].schema == {}


@pytest.mark.asyncio
async def test_list_tools_propagates_http_error():
    response = MagicMock()
    response.raise_for_status.side_effect = RuntimeError("request failed")

    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.get = AsyncMock(return_value=response)

    with patch(
        "bindai_mcp.client.httpx.AsyncClient",
        return_value=mock_client,
    ):
        with pytest.raises(
            RuntimeError,
            match="request failed",
        ):
            await MCPClient("http://localhost:8000").list_tools()


def test_tool_definition():
    client = MCPClient("http://localhost:8000")
    tool = MCPTool(
        client=client,
        name="search",
        description="Search documents",
        schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
        },
    )

    definition = tool.definition

    assert definition.name == "search"
    assert definition.description == "Search documents"
    assert definition.parameters["properties"]["query"]["type"] == "string"


def test_tool_execute():
    client = MCPClient("http://localhost:8000")
    tool = MCPTool(
        client=client,
        name="search",
        description="Search documents",
        schema={},
    )

    context = MagicMock()
    context.variables = {"query": "BindAI"}

    response = MagicMock()
    response.json.return_value = {"results": ["BindAI documentation"]}
    response.raise_for_status.return_value = None

    with patch(
        "bindai_mcp.client.httpx.post",
        return_value=response,
    ) as mock_post:
        result = tool.execute(context)

    mock_post.assert_called_once_with(
        "http://localhost:8000/call",
        json={
            "tool": "search",
            "arguments": {"query": "BindAI"},
        },
    )

    response.raise_for_status.assert_called_once_with()

    assert result.success is True
    assert result.output == {"results": ["BindAI documentation"]}


def test_tool_execute_without_variables_uses_empty_arguments():
    client = MCPClient("http://localhost:8000")
    tool = MCPTool(
        client=client,
        name="ping",
        description="Ping",
    )

    context = object()

    response = MagicMock()
    response.json.return_value = {"ok": True}
    response.raise_for_status.return_value = None

    with patch(
        "bindai_mcp.client.httpx.post",
        return_value=response,
    ) as mock_post:
        result = tool.execute(context)

    mock_post.assert_called_once_with(
        "http://localhost:8000/call",
        json={
            "tool": "ping",
            "arguments": {},
        },
    )

    assert result.success is True
    assert result.output == {"ok": True}


def test_tool_execute_propagates_http_error():
    client = MCPClient("http://localhost:8000")
    tool = MCPTool(
        client=client,
        name="search",
        description="Search documents",
    )

    context = MagicMock()
    context.variables = {"query": "BindAI"}

    response = MagicMock()
    response.raise_for_status.side_effect = RuntimeError("request failed")

    with patch(
        "bindai_mcp.client.httpx.post",
        return_value=response,
    ):
        with pytest.raises(
            RuntimeError,
            match="request failed",
        ):
            tool.execute(context)