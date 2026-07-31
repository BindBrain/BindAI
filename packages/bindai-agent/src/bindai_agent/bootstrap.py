from bindai_core.container import BindContainer

from .execution.finish_step import FinishStep
from .execution.knowledge_step import KnowledgeStep
from .execution.memory_step import MemoryStep
from .execution.prompt_builder import PromptBuilder
from .execution.tool_executor import ToolExecutor


def register_agent_services(
    container: BindContainer,
):

    container.register(
        MemoryStep,
        MemoryStep(),
    )

    container.register(
        KnowledgeStep,
        KnowledgeStep(),
    )

    container.register(
        PromptBuilder,
        PromptBuilder(),
    )

    container.register(
        ToolExecutor,
        ToolExecutor(),
    )

    container.register(
        FinishStep,
        FinishStep(),
    )
