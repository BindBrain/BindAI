from bindai_core import Tool, ToolResult


class GreetingTool(Tool):

    @property
    def name(self):
        return "greet"

    @property
    def description(self):
        return "Greets a person."

    def execute(self, person_name: str):
        return ToolResult(
            output=f"Hello {person_name}",
        )


tool = GreetingTool()

print(tool.definition())