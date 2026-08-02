"""
23 MCP Demo Server

Provides tools for BindAI MCP client.
"""

from fastapi import FastAPI

app = FastAPI(title="BindAI MCP Demo Server")


@app.get("/mcp/tools")
def tools():

    return [
        {"name": "calculator", "description": ("Adds two numbers")},
        {"name": "weather", "description": ("Returns fake weather information")},
    ]


@app.post("/mcp/call")
def call_tool(payload: dict):

    tool = payload["tool"]

    args = payload.get(
        "arguments",
        {},
    )

    if tool == "calculator":
        return {"result": args["a"] + args["b"]}

    if tool == "weather":
        return {"result": "Sunny, 25C"}

    return {"error": "Unknown tool"}
