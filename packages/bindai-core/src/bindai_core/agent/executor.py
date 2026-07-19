from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
)
from bindai_core.events import (
    Event,
    EventTypes,
)

from .agent import Agent
from .result import AgentResult
from .state import AgentState


class AgentExecutor:
    """
    Executes an Agent.

    Responsibilities

    - build prompt
    - inject memory
    - inject knowledge
    - execute middleware
    - call provider
    - execute tool calls
    - update conversation
    - return AgentResult
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

            agent.state = AgentState.RUNNING

            #
            # Middleware (before)
            #

            for middleware in agent.middleware:

                middleware.before(
                    agent,
                    context,
                )

            #
            # Build request
            #

            request = self._build_request(
                agent,
                context,
            )

            #
            # Provider call
            #

            response = agent.provider.generate(
                request,
            )

            #
            # Tool calls
            #

            if response.tool_calls:

                self._execute_tools(
                    agent,
                    context,
                    response,
                )

            #
            # Conversation
            #

            self._update_conversation(
                agent,
                context,
                response,
            )

            #
            # Middleware (after)
            #

            result = AgentResult(

                success=True,

                output=response.content,

            )

            for middleware in agent.middleware:

                middleware.after(
                    agent,
                    context,
                    result,
                )

            #
            # Publish event
            #

            context.events.publish(

                Event(

                    name=EventTypes.AGENT_FINISHED,

                    payload={

                        "agent": agent.name,

                    },

                )

            )

            agent.state = AgentState.COMPLETED

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
    # Request builder
    #

    def _build_request(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> ModelRequest:

        messages = []

        #
        # System
        #

        messages.append(

            Message(

                role=MessageRole.SYSTEM,

                content=agent.instructions,

            )

        )

        #
        # Memory
        #

        if agent.memory is not None:

            messages.extend(

                agent.memory.messages()

            )

        #
        # Conversation
        #

        messages.extend(

            agent.conversation.messages

        )

        #
        # User
        #

        messages.append(

            Message(

                role=MessageRole.USER,

                content=context.variables.get(
                    "message",
                ),

            )

        )

        return ModelRequest(

            messages=messages,

            tools=agent.tools.all(),

            temperature=agent.configuration.temperature,

            max_tokens=agent.configuration.max_tokens,

        )

    #
    # Execute tool calls
    #

    def _execute_tools(
        self,
        agent: Agent,
        context: ExecutionContext,
        response,
    ):

        for call in response.tool_calls:

            tool = agent.tools.get(
                call.name,
            )

            result = tool.invoke(
                **call.arguments,
            )

            context.variables.set(

                call.name,

                result,

            )

    #
    # Conversation update
    #

    def _update_conversation(
        self,
        agent: Agent,
        context: ExecutionContext,
        response,
    ):

        user = context.variables.get(
            "message",
        )

        if user is not None:

            agent.conversation.add_user(
                user,
            )

        agent.conversation.add_assistant(

            response.content,

        )