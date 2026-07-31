from agents.assistant import agent

print("\nLoaded tools:\n")

for tool in agent.tools.all():
    print("-", tool.name)