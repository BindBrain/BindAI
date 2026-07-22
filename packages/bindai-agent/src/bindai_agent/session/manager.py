from __future__ import annotations

from .session import AgentSession


class SessionManager:
    def create(
        self,
        agent,
    ) -> AgentSession:

        return AgentSession(
            agent,
        )
