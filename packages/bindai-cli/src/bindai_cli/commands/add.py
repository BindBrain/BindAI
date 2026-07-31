from pathlib import Path

from ..app import app
from ..generators import (
    generate_agent,
    generate_tool,
    generate_workflow,
)


@app.command("agent")
def add_agent(name: str):
    generate_agent(Path.cwd(), name)


@app.command("tool")
def add_tool(name: str):
    generate_tool(Path.cwd(), name)


@app.command("workflow")
def add_workflow(name: str):
    generate_workflow(Path.cwd(), name)
