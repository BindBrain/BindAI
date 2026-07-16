class AgentRegistry:

    def __init__(self):

        self._agents = {}

    def register(self, agent):

        self._agents[agent.name] = agent

    def get(self, name):

        return self._agents[name]

    def exists(self, name):

        return name in self._agents

    def all(self):

        return list(self._agents.values())