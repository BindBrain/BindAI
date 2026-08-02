"""
29 Production Project Layout

Demonstrates a recommended production
structure for BindAI applications.

Concepts:
- Application organization
- Separation of concerns
- Agents
- Workflows
- Tools
- Memory
- Knowledge
- Configuration

This example is a blueprint,
not a standalone execution script.
"""

PROJECT_STRUCTURE = """
my-bindai-application/

├── agents/
│   ├── research_agent.py
│   ├── support_agent.py
│   └── planner_agent.py
│
├── workflows/
│   ├── research_flow.py
│   ├── approval_flow.py
│   └── automation_flow.py
│
├── tools/
│   ├── database.py
│   ├── search.py
│   └── api.py
│
├── memory/
│   ├── provider.py
│   └── storage.py
│
├── knowledge/
│   ├── loaders.py
│   ├── embeddings.py
│   └── retrievers.py
│
├── config/
│   ├── settings.yaml
│   └── providers.yaml
│
├── api/
│   └── server.py
│
├── tests/
│
├── main.py
│
└── pyproject.toml
"""


def main():

    print("Recommended BindAI Production Layout\n")

    print(PROJECT_STRUCTURE)

    print(
        """
Architecture principles:

✓ Keep agents focused
✓ Separate tools from business logic
✓ Isolate providers
✓ Store configuration externally
✓ Test workflows independently
✓ Keep applications modular
"""
    )


if __name__ == "__main__":
    main()
