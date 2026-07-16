from bindai_core import Tool, ToolResult


class GreetingTool(Tool):

    @property
    def name(self):
        return "greet"

    @property
    def description(self):
        return "Greets a user."

    @property
    def parameters(self):
        return {
            "person_name": {
                "type": "string",
                "description": "Name of the person.",
            }
        }

    def execute(self, person_name):
        return ToolResult(
            output=f"Hello {person_name}",
        )


tool = GreetingTool()

print(tool.name)
print(tool.description)
print(tool.parameters)