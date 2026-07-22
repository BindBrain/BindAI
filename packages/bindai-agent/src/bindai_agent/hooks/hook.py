from __future__ import annotations

from abc import ABC


class AgentHook(ABC):
    """
    Lifecycle hooks.

    Override only the methods you need.
    """

    def on_start(
        self,
        agent,
        context,
    ):
        pass

    def on_model_request(
        self,
        request,
    ):
        pass

    def on_model_response(
        self,
        response,
    ):
        pass

    def on_tool_start(
        self,
        agent,
        tool_call,
    ):
        pass

    def on_tool_end(
        self,
        agent,
        tool_call,
        result,
    ):
        pass

    def on_finish(
        self,
        result,
    ):
        pass

    def on_error(
        self,
        exception,
    ):
        pass
