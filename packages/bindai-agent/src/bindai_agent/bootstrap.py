from bindai_core.container import BindContainer

from .execution.memory_step import MemoryStep
from .execution.knowledge_step import KnowledgeStep
from .execution.prompt_builder import PromptBuilder
from .execution.tool_executor import ToolExecutor
from .execution.finish_step import FinishStep


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
