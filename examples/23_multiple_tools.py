"""
23 MCP Tool Integration

Demonstrates connecting BindAI with
Model Context Protocol (MCP) tools.

Concepts:
- MCP client connection
- External tool discovery
- Tool registration
- Agent execution
"""

import asyncio

from bindai import AgentBuilder
from bindai_mcp import MCPClient


async def main():
    # Connect to an MCP server.
    #
    # This example assumes an MCP server exposing tools.
    # Replace the URL with your MCP server.
    client = MCPClient(url="http://localhost:8000/mcp")

    # Discover available tools
    tools = await client.list_tools()

    print("Available MCP tools:")

    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

    # Create an agent with MCP tools
    agent = (
        AgentBuilder()
        .openai("gpt-4.1-mini")
        .instructions(
            """
            You are an assistant with access
            to external MCP tools.
            Use tools when required.
            """
        )
        .tools(*tools)
        .build()
    )

    # Execute request
    result = agent.chat("What tools are available and what can they do?")

    print("\nResponse:")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
