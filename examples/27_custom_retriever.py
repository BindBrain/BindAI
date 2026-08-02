"""
27 Scheduled Agent

Demonstrates running an AI agent on a schedule.

Concepts:
- Automated execution
- Scheduled tasks
- Background agents
- Periodic reporting

Production use cases:
- Daily reports
- Monitoring
- Data analysis
- Automation jobs
"""

import asyncio
from datetime import datetime

from bindai import AgentBuilder

agent = (
    AgentBuilder()
    .openai("gpt-4.1-mini")
    .instructions(
        """
        You are a scheduled automation agent.

        Generate concise daily reports.
        """
    )
    .build()
)


async def run_scheduled_task():

    result = agent.chat(
        """
        Create a daily AI system report.

        Include:
        - Summary
        - Important events
        - Recommended actions
        """
    )

    print(
        f"""
Scheduled execution:
{datetime.now()}

Report:
{result.output}
"""
    )


async def scheduler():
    """
    Demo scheduler.

    Runs a limited number of times.

    Production applications can use:

    - APScheduler
    - Celery
    - Cron
    - Cloud schedulers
    """

    runs = 3

    for _ in range(runs):
        await run_scheduled_task()

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(scheduler())
