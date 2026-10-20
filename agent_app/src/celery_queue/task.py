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

TELEGRAM_MAX_MESSAGE_LENGTH = 4096
TELEGRAM_SAFE_MESSAGE_LENGTH = 3800


def _split_text(text: str, max_length: int = TELEGRAM_SAFE_MESSAGE_LENGTH):
    """Split text into Telegram-safe chunks, preferring natural boundaries."""
    remaining = text.strip()

    while remaining:
        if len(remaining) <= max_length:
            yield remaining
            return

        split_at = remaining.rfind("\n", 0, max_length + 1)
        if split_at <= 0:
            split_at = remaining.rfind(" ", 0, max_length + 1)
        if split_at <= 0:
            split_at = max_length

        chunk = remaining[:split_at].rstrip()
        if not chunk:
            chunk = remaining[:max_length]
            split_at = max_length

        yield chunk
        remaining = remaining[split_at:].lstrip()


def _render_for_telegram(text: str):
    rendered_text, entities = convert(text)

    # Conversion can expand Markdown. Fall back to plain text if the rendered
    # result still exceeds Telegram's hard limit.
    if len(rendered_text) > TELEGRAM_MAX_MESSAGE_LENGTH:
        return text, []

    return rendered_text, [entity.to_dict() for entity in entities]

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
                            draft_text = full_text
                            if len(draft_text) > TELEGRAM_SAFE_MESSAGE_LENGTH:
                                draft_text = (
                                    draft_text[:TELEGRAM_SAFE_MESSAGE_LENGTH - 1].rstrip()
                                    + "…"
                                )

                            rendered_text, entities = _render_for_telegram(draft_text)

                            await bot.send_message_draft(
                                chat_id=chat_id,
                                draft_id=draft_id,
                                text=rendered_text,
                                entities=entities,
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
                if full_text.strip():
                    for message_part in _split_text(full_text):
                        rendered_text, entities = _render_for_telegram(message_part)
                        await bot.send_message(
                            chat_id=chat_id,
                            text=rendered_text,
                            entities=entities,
                        )

            except Exception:
                logger.exception("Falha durante a execução do agente no thread %s", thread_id)
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Não foi possível concluir ou entregar a resposta. Verifique o estado da operação antes de repetir.",
                    )
                except Exception:
                    logger.exception("Não foi possível enviar a mensagem de erro ao thread %s", thread_id)

                return {
                    "status": "failed",
                    "thread_id": thread_id,
                    "reason": "agent_execution_error",
                }

            return {
                "status": "completed",
                "thread_id": thread_id,
            }
