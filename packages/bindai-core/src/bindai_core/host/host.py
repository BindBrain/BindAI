from __future__ import annotations

from bindai_core.application import BindApplication
from bindai_core.container import BindContainer
from bindai_core.context import ExecutionContext
from bindai_core.events import EventBus
from bindai_core.registry import Registry

from bindai_core.provider import ProviderManager

from bindai_core.managers import (
    ToolManager,
    AgentManager,
    WorkflowManager,
    MemoryManager,
    MCPManager,
    TriggerManager,
)


class BindHost:
    """
    Central object representing a running BindAI application.
    """

    def __init__(self, application: BindApplication):

        self.application = application

        # Core
        self.context = ExecutionContext()
        self.container = BindContainer()
        self.events = EventBus()
        self.registry = Registry()

        # Managers
        self.providers = ProviderManager()
        self.tools = ToolManager()
        self.agents = AgentManager()
        self.workflows = WorkflowManager()
        self.memory = MemoryManager()
        self.mcp = MCPManager()
        self.triggers = TriggerManager()

    def register(self, key: str, value: object):
        self.registry.register(key, value)
        return self

    def publish(self, event):
        self.events.publish(event)
        return self

    def resolve(self, service):
        return self.container.resolve(service)