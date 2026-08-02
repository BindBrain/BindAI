"""
28 Event Driven Agent

Demonstrates triggering AI agents from events.

Concepts:
- Event based execution
- Agent triggers
- Event payload handling
- Automated responses

Production use cases:
- Webhooks
- Message queues
- User events
- System notifications
"""

import asyncio
from datetime import datetime
from typing import Any

from bindai import AgentBuilder


class Event:
    def __init__(
        self,
        name: str,
        payload: dict[str, Any],
    ):
        self.name = name
        self.payload = payload
        self.timestamp = datetime.now()


class EventBus:
    """
    Simple event bus example.

    Production alternatives:

    - Kafka
    - RabbitMQ
    - Redis Streams
    - AWS EventBridge
    """

    def __init__(self):
        self.handlers = {}

    def subscribe(
        self,
        event_name: str,
        handler,
    ):
        self.handlers[event_name] = handler

    async def publish(
        self,
        event: Event,
    ):

        handler = self.handlers.get(event.name)

        if handler:
            await handler(event)


#
# Create agent once.
# In production this would normally
# be a shared service instance.
#

agent = (
    AgentBuilder()
    .openai("gpt-4.1-mini")
    .instructions(
        """
        You are an event processing agent.

        Analyze incoming events and
        suggest useful actions.
        """
    )
    .build()
)


async def agent_handler(
    event: Event,
):

    result = agent.chat(
        f"""
        Event:

        Name:
        {event.name}

        Timestamp:
        {event.timestamp}

        Data:
        {event.payload}

        Analyze this event and
        suggest appropriate actions.
        """
    )

    print("\nAgent Event Response:")

    print(result.output)


async def main():

    bus = EventBus()

    #
    # Register event handler
    #

    bus.subscribe(
        "user.created",
        agent_handler,
    )

    #
    # Create event
    #

    event = Event(
        name="user.created",
        payload={
            "user_id": "123",
            "plan": "enterprise",
        },
    )

    print("Publishing event...")

    await bus.publish(event)


if __name__ == "__main__":
    asyncio.run(main())
