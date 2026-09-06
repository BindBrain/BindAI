from __future__ import annotations

from typing import cast

from bindai_core.context import ExecutionContext
from bindai_core.events.agent_events import AgentFinishedEvent
from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
    ModelResponse,
)

from .agent import Agent
from .result import AgentResult
from .state import AgentState


class AgentExecutor:
    """
    Executes an Agent.

    Execution pipeline

        prepare
            ↓
        middleware(before)
            ↓
        run until complete
            ↓
        middleware(after)
            ↓
        publish event
            ↓
        complete
    """

    #
    # Public
    #

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> AgentResult:

        try:
            self._prepare(agent)

            self._run_before_middleware(
                agent,
                context,
            )

            #
            # Insert the initial user message exactly once.
            #

            user = context.variables.get("message")

            if user is not None:
                agent.conversation.add_user(
                    user,
                )

            response = self._run_until_complete(
                agent,
                context,
            )

            result = AgentResult(
                success=True,
                output=response.content,
            )

            self._run_after_middleware(
                agent,
                context,
                result,
            )

            self._publish_finished_event(
                agent,
                context,
            )

            self._complete(agent)

            return result

        except Exception as ex:
            agent.state = AgentState.FAILED

            return AgentResult(
                success=False,
                error=str(ex),
            )

    #
    # Streaming
    #

    def stream(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):

        request = self._build_request(
            agent,
            context,
        )

        return agent.provider.stream(
            request,
        )

    #
    # Execution Loop
    #

    def _run_until_complete(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ModelResponse:

        iterations = 0

        while True:
            response = self._execute_turn(
                agent,
                context,
            )

            #
            # Finished
            #

            if not response.tool_calls:
                return response

            iterations += 1

            if iterations >= agent.configuration.max_tool_iterations:
                raise RuntimeError(
                    "Maximum tool iterations exceeded."
                )

    def _execute_turn(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ModelResponse:

        request = self._build_request(
            agent,
            context,
        )

        response = self._call_provider(
            agent,
            request,
        )

        tool_messages = self._execute_tools(
            agent,
            context,
            response,
        )

        self._append_tool_messages(
            agent,
            tool_messages,
        )

        self._update_conversation(
            agent,
            context,
            response,
        )

        return response

    #
    # Pipeline
    #

    def _prepare(
        self,
        agent: Agent,
    ):

        agent.state = AgentState.RUNNING

    def _complete(
        self,
        agent: Agent,
    ):

        agent.state = AgentState.COMPLETED

    def _run_before_middleware(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):

        for middleware in agent.middleware:
            middleware.before_execute(
                agent,
                context,
            )

    def _run_after_middleware(
        self,
        agent: Agent,
        context: ExecutionContext,
        result: AgentResult,
    ):

        for middleware in agent.middleware:
            middleware.after_execute(
                agent,
                context,
                result,
            )

    def _call_provider(
        self,
        agent: Agent,
        request: ModelRequest,
    ) -> ModelResponse:

        response = agent.provider.generate(
            request,
        )

        return cast(
            ModelResponse,
            response,
        )

    def _publish_finished_event(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):

        context.events.publish(
            AgentFinishedEvent(
                payload={
                    "agent": agent.name,
                },
            )
        )

    #
    # Request Builder
    #

    def _retrieve_context(
        self,
        agent: Agent,
    ) -> str:

        if agent.knowledge is not None:
            result = agent.knowledge.search_conversation(
                agent.conversation,
                limit=5,
            )

            if result.success and result.value:
                return "\n\n".join(
                    document.content
                    for document in result.value
                )

            return ""

        if agent.retriever is not None:
            query = ""

            if agent.conversation.messages:
                query = agent.conversation.messages[-1].content

            if not query:
                return ""

            result = agent.retriever.retrieve(
                query,
                top_k=5,
            )

            if result.success and result.documents:
                return "\n\n".join(
                    document.content
                    for document in result.documents
                )

        return ""

    def _build_request(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ModelRequest:

        messages: list[Message] = []

        messages.append(
            Message(
                role=MessageRole.SYSTEM,
                content=agent.instructions,
            )
        )

        messages.extend(
            agent.conversation.messages
        )

        context_text = self._retrieve_context(
            agent,
        )

        if context_text:
            messages.append(
                Message(
                    role=MessageRole.SYSTEM,
                    content=(
                        "Relevant knowledge context:\n\n"
                        f"{context_text}"
                    ),
                )
            )

        return ModelRequest(
            messages=messages,
            tools=agent.tools.definitions(),
            temperature=agent.configuration.temperature,
            max_tokens=agent.configuration.max_tokens,
        )

    #
    # Tool Calls
    #

    def _execute_tools(
        self,
        agent: Agent,
        context: ExecutionContext,
        response: ModelResponse,
    ) -> list[Message]:

        messages: list[Message] = []

        if not response.tool_calls:
            return messages

        for call in response.tool_calls:
            tool = agent.tools.get(
                call.name,
            )

            #
            # Build tool execution context
            #

            tool_context = ExecutionContext()

            for key, value in call.arguments.items():
                tool_context.variables.set(
                    key,
                    value,
                )

            result = tool.execute(
                tool_context,
            )

            #
            # Store in execution context
            #

            context.variables.set(
                call.name,
                result,
            )

            #
            # Build Tool Message
            #

            output = ""

            if result.value is not None:
                output = str(result.value)

            elif result.error is not None:
                output = result.error

            messages.append(
                Message(
                    role=MessageRole.TOOL,
                    content=output,
                    tool_call_id=getattr(
                        call,
                        "id",
                        None,
                    ),
                )
            )

        return messages

    def _append_tool_messages(
        self,
        agent: Agent,
        messages: list[Message],
    ):

        for message in messages:
            if message.role == MessageRole.ASSISTANT:

                if message.tool_calls:
                    agent.conversation.add_assistant_tool_call(
                        message.tool_calls,
                    )

                else:
                    agent.conversation.add_assistant(
                        message.content,
                    )

            elif message.role == MessageRole.TOOL:
                agent.conversation.add_tool(
                    tool_call_id=message.tool_call_id or "",
                    content=message.content,
                )

            elif message.role == MessageRole.USER:
                agent.conversation.add_user(
                    message.content,
                )

            elif message.role == MessageRole.SYSTEM:
                agent.conversation.add_system(
                    message.content,
                )

    def _update_conversation(
        self,
        agent: Agent,
        context: ExecutionContext,
        response: ModelResponse,
    ):

        agent.conversation.add_assistant(
            response.content,
        )

        if response.tool_calls:
            agent.conversation.add_assistant_tool_call(
                response.tool_calls,
            )