class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name):
        return self._tools[name]

    def exists(self, name):
        return name in self._tools

    def list(self):
        return list(self._tools.values())

    # Optional backward compatibility
    def all(self):
        return self.list()