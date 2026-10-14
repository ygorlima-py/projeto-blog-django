import asyncio
from typing import Any

from agent import AgentBase
from checkpointer.postgres_checkpointer import start_postgres_checkpointer
from infra import load_llm
from config import load_settings

settings = load_settings()

async def _run_telegram_agent(
    user_input: str,
    thread_id: str,
    agent: type[AgentBase],
) -> dict[str, Any]:
    chunks: list[str] = []
    interruption = None

        
    async with start_postgres_checkpointer() as checkpointer:
        graph = agent(
            model=load_llm(),
            checkpointer=checkpointer,
        )

        async for event in graph.astream(
            user_input=user_input,
            thread_id=thread_id,
        ):
            if event["type"] == "token":
                token = event["content"]
                chunks.append(token)

                # Depois substitua pelo envio ao Telegram
                print(token, end="", flush=True)

            elif event["type"] == "interrupt":
                interruption = event["data"]

    if interruption is not None:
        return {
            "status": "interrupted",
            "thread_id": thread_id,
            "interrupt": interruption,
        }

    return {
        "status": "completed",
        "thread_id": thread_id,
        "content": "".join(chunks),
    }