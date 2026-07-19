class AgentError(Exception):
    pass


class AgentExecutionError(AgentError):
    pass


class AgentConfigurationError(AgentError):
    pass