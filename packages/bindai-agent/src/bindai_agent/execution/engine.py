from __future__ import annotations

from .knowledge_step import KnowledgeStep
from .memory_step import MemoryStep
from .prompt_builder import PromptBuilder
from .result import ExecutionResult
from .tool_loop import ToolLoop


class AgentExecutionEngine:
    """
    Central runtime responsible for
    coordinating agent execution.
    """

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

        self.prompt_builder = PromptBuilder()

        self.knowledge = KnowledgeStep()

        self.memory = MemoryStep()

        self.tools = ToolLoop()

    def run(
        self,
        user_input: str,
    ) -> ExecutionResult:
        """
        Placeholder implementation.

        The full execution loop
        will be implemented in
        the next steps.
        """

        prompt = self.prompt_builder.build(
            user_input,
        )

        return ExecutionResult(
            success=True,
            response=prompt,
            iterations=1,
        )