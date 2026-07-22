from bindai_core import Tool, ToolResult


class GreetingTool(Tool):
    @property
    def name(self):
        return "greet"

    def execute(
        self,
        person_name: str,
        age: int,
        premium: bool,
    ):
        return ToolResult(
            output="ok",
        )


tool = GreetingTool()

print(tool.parameters)
