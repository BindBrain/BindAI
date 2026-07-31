from bindai_agent import AgentRegistry
from bindai_model import ModelRegistry


class ApplicationRegistry:
    def __init__(self):

        self.models = ModelRegistry()

        self.agents = AgentRegistry()
