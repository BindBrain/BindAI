from bindai_core import Bind

app = Bind.create("BindAI")

print("Application:", app.application.name)
print("Version:", app.application.version)

print("Provider Manager :", type(app.providers).__name__)
print("Tool Manager     :", type(app.tools).__name__)
print("Agent Manager    :", type(app.agents).__name__)
print("Workflow Manager :", type(app.workflows).__name__)
print("Memory Manager   :", type(app.memory).__name__)
print("MCP Manager      :", type(app.mcp).__name__)
print("Trigger Manager  :", type(app.triggers).__name__)