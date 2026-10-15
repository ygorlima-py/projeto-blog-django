from __future__ import annotations
from celery import Celery
from typing import Any, Literal

from agent import SupervisoryAgent
from celery_queue.task import _run_telegram_agent
from config import load_settings

import asyncio

settings = load_settings()

app = Celery(
    "agent_app",
    broker=settings.uri_broker,
)

@app.task(name="agent.run_telegram_agent")
def run_telegram_agent(
    user_input: str,
    thread_id: str,
    type: Literal["text", "decision"],
    ) -> dict[str, Any]:
    
    return asyncio.run(_run_telegram_agent(user_input, thread_id, _type=type, agent=SupervisoryAgent))





