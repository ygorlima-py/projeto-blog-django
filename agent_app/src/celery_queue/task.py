from typing import Any, Literal
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegramify_markdown import convert

import logging
import secrets
import time

from langgraph.types import Command

from agent import AgentBase
from checkpointer.postgres_checkpointer import start_postgres_checkpointer
from infra import load_llm
from config import load_settings

settings = load_settings()
logger = logging.getLogger(__name__)

async def _run_telegram_agent(
        user_input: str | Command,
        thread_id: str,
        _type: Literal["text", "decision"],
        agent: type[AgentBase],
    ) -> dict[str, Any]:
    
    interruption = None
    
    if _type == "decision":
        if user_input == "hitl:approve":
            user_input = Command(
                resume={
                    "decisions": [
                        {"type": "approve"}
                    ]
                }
            )
        else:
            user_input = Command(
                resume={
                    "decisions": [
                        {"type": "reject"}
                    ]
                }
            )

    async with start_postgres_checkpointer() as checkpointer:
        
        if not settings.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not configurated")
        
        draft_id = secrets.randbits(63) or 1
        full_text = ""
        last_draft_at = 0.0
        chat_id = int(thread_id)

        graph = agent(
            model=load_llm(),
            checkpointer=checkpointer,
        )
        
        async with Bot(token=settings.telegram_token) as bot:
            try:
                async for event in graph.astream(
                    user_input=user_input,
                    thread_id=thread_id,
                ):
                    if event["type"] == "chunk":
                        chunk = event["content"]
                        full_text += chunk

                        now = time.monotonic()
                        if now - last_draft_at >= 1.0:
                            rendered_text, entities = convert(full_text)

                            await bot.send_message_draft(
                                chat_id=chat_id,
                                draft_id=draft_id,
                                text=rendered_text,
                                entities=[entity.to_dict() for entity in entities],
                            )
                            last_draft_at = now

                    elif event["type"] == "interrupt":
                        interruption = event["data"]

                        if interruption is not None:
                            action = interruption["action_requests"][0]
                            allowed = interruption["review_configs"][0]["allowed_decisions"]

                            buttons = []

                            if "approve" in allowed:
                                buttons.append(
                                    InlineKeyboardButton(
                                        "Aprovar",
                                        callback_data="hitl:approve",
                                    )
                                )

                            if "reject" in allowed:
                                buttons.append(
                                    InlineKeyboardButton(
                                        "Rejeitar",
                                        callback_data="hitl:reject",
                                    )
                                )

                            await bot.send_message(
                                    chat_id=chat_id,
                                    text=f"A ferramenta `{action['name']}` precisa de aprovação.",
                                    reply_markup=InlineKeyboardMarkup([buttons]),
                                )

                            return {
                                    "status": "interrupted",
                                    "thread_id": thread_id,
                                    "interrupt": interruption,
                                    }
            except Exception:
                logger.exception("Falha durante a execução do agente no thread %s", thread_id)
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="A conexão com a ferramenta foi encerrada e não foi possível confirmar o resultado. Verifique o estado da operação antes de repetir.",
                    )
                except Exception:
                    logger.exception("Não foi possível enviar a mensagem de erro ao thread %s", thread_id)

                return {
                    "status": "failed",
                    "thread_id": thread_id,
                    "reason": "agent_execution_error",
                }
                    
            rendered_text, entities = convert(full_text)

            if rendered_text.strip():
                await bot.send_message(
                            chat_id=chat_id,
                            text=rendered_text,
                            entities=[entity.to_dict() for entity in entities],
                        )
            elif full_text.strip():
                await bot.send_message(
                            chat_id=chat_id,
                            text=full_text,
                        )

            return {
                "status": "completed",
                "thread_id": thread_id,
            }
