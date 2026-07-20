from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)
from bindai_core.schema import SchemaSerializer

from .output.parser import OutputParser
from .result import AgentResult

if TYPE_CHECKING:
    from .agent import Agent


class AgentExecutor:
    """
    Executes an agent by driving the full execution loop.
    """

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> AgentResult:

        self._initialize(
            agent,
            context,
        )

        for middleware in agent.middleware:

            middleware.before_execute(
                agent,
                context,
            )

        for hook in agent.hooks:

            hook.on_start(
                agent,
                context,
            )

        while True:

            request = self._build_request(
                agent,
                context,
            )

            for hook in agent.hooks:

                hook.on_model_request(
                    request,
                )

            response = self._generate(
                agent,
                request,
            )

            for hook in agent.hooks:

                hook.on_model_response(
                    response,
                )

            if not response.tool_calls:

                result = self._finish(
                    agent,
                    context,
                    response,
                )

                for middleware in reversed(
                    agent.middleware,
                ):

                    middleware.after_execute(
                        agent,
                        context,
                        result,
                    )

                return result

            self._execute_tool_calls(
                agent,
                response,
            )

    def stream(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):

        self._initialize(
            agent,
            context,
        )

        request = self._build_request(
            agent,
            context,
        )

        content = ""

        for chunk in agent.provider.stream(
            request,
        ):

            content += chunk.delta

            yield chunk

        agent.conversation.add_assistant(
            content,
        )

    def _initialize(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> None:

        user_input = context.variables.get(
            "input",
            "",
        )

        if len(agent.conversation) == 0:

            agent.conversation.add_system(
                agent.instructions,
            )

            self._load_memory(
                agent,
            )

        agent.conversation.add_user(
            user_input,
        )

        if agent.knowledge is not None:

            context_text = agent.knowledge.retrieve(
                user_input,
            )

            if context_text:

                agent.conversation.add_system(
                    f"Relevant knowledge:\n{context_text}",
                )

    def _load_memory(
        self,
        agent: Agent,
    ) -> None:

        result = agent.memory.get(
            "__context__",
        )

        if not result.success:
            return

        record = result.value

        if record is None:
            return

        agent.conversation.add_system(
            f"Relevant memory:\n{record.value}",
        )

    def _save_memory(
        self,
        agent: Agent,
    ) -> None:

        transcript = []

        for message in agent.conversation.messages:

            transcript.append(
                f"{message.role.value}: {message.content}"
            )

        from bindai_memory import MemoryRecord

        agent.memory.set(
            MemoryRecord(
                key="__context__",
                value="\n".join(
                    transcript,
                ),
            )
        )

    def _build_request(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ModelRequest:

        request = agent.conversation.to_request()

        request.tools = agent.tools.definitions()

        output_type = context.variables.get(
            "output_type",
        )

        if output_type is not None:

            request.response_schema = (
                SchemaSerializer.serialize(
                    output_type,
                )
            )

        return request

    def _generate(
        self,
        agent: Agent,
        request: ModelRequest,
    ) -> ModelResponse:

        return agent.provider.generate(
            request,
        )

    def _execute_tool_calls(
        self,
        agent: Agent,
        response: ModelResponse,
    ) -> None:

        agent.conversation.add_assistant_tool_call(
            response.tool_calls,
        )

        for tool_call in response.tool_calls:

            #
            # Hook: before tool execution
            #

            for hook in agent.hooks:

                hook.on_tool_start(
                    tool_call,
                )

            result = agent.execute_tool(
                tool_call.name,
                **tool_call.arguments,
            )

            #
            # Hook: after tool execution
            #

            for hook in agent.hooks:

                hook.on_tool_end(
                    tool_call,
                    result,
                )

            agent.conversation.add_tool(
                tool_call_id=tool_call.id,
                content=(
                    str(result.output)
                    if result.success
                    else f"ERROR: {result.error}"
                ),
            )

    def _finish(
        self,
        agent: Agent,
        context: ExecutionContext,
        response: ModelResponse,
    ) -> AgentResult:

        agent.conversation.add_assistant(
            response.content,
        )

        self._save_memory(
            agent,
        )

        output_type = context.variables.get(
            "output_type",
        )

        output = OutputParser.parse(
            response.content,
            output_type,
        )

        result = AgentResult(
            success=True,
            output=output,
        )

        #
        # Notify hooks
        #

        for hook in agent.hooks:

            hook.on_finish(
                result,
            )

        return result