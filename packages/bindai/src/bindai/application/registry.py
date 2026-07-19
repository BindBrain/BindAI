from bindai_agent import AgentRegistry
from bindai_model import ProviderRegistry


class ApplicationRegistry:

    def __init__(self):

        self.providers = ProviderRegistry()

        self.agents = AgentRegistry()