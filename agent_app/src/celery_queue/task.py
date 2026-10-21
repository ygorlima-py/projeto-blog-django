from typing import Any, Literal
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError
from telegramify_markdown import convert

import logging
import secrets
import time
from contextlib import nullcontext

from langgraph.types import Command

from agent import AgentBase
from checkpointer.postgres_checkpointer import start_postgres_checkpointer
from infra import load_llm
from config import load_settings

settings = load_settings()
logger = logging.getLogger(__name__)

TELEGRAM_MAX_MESSAGE_LENGTH = 4096
TELEGRAM_SAFE_MESSAGE_LENGTH = 3800
MAX_CONSECUTIVE_WHITESPACE_CHUNKS = 100


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
    plain_text = text.strip()
    if not plain_text:
        return "", []

    # Markdown rendering is optional: delivery must still work when conversion
    # fails or produces an empty/oversized Telegram message.
    try:
        rendered_text, entities = convert(plain_text)
        rendered_entities = [entity.to_dict() for entity in entities]
    except Exception:
        logger.warning("Telegram Markdown conversion failed; using plain text", exc_info=True)
        return plain_text, []

    if not rendered_text.strip() or len(rendered_text) > TELEGRAM_MAX_MESSAGE_LENGTH:
        return plain_text, []

    return rendered_text, rendered_entities


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

    checkpointer_context = (
        start_postgres_checkpointer()
        if settings.checkpointer
        else nullcontext(None)
    )

    async with checkpointer_context as checkpointer:
        
        if not settings.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not configurated")
        
        draft_id = secrets.randbits(63) or 1
        full_text = ""
        pending_whitespace = ""
        consecutive_whitespace_chunks = 0
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
                        if not isinstance(chunk, str) or not chunk:
                            continue

                        # Buffer whitespace until real content arrives. This keeps
                        # word boundaries without treating endless spaces as output.
                        if chunk.isspace():
                            consecutive_whitespace_chunks += 1
                            if (
                                consecutive_whitespace_chunks
                                > MAX_CONSECUTIVE_WHITESPACE_CHUNKS
                            ):
                                raise RuntimeError("Agent stream produced only whitespace")

                            if full_text:
                                whitespace = pending_whitespace + chunk
                                pending_whitespace = (
                                    "\n\n" if "\n\n" in whitespace
                                    else "\n" if "\n" in whitespace
                                    else " "
                                )
                            continue

                        consecutive_whitespace_chunks = 0
                        full_text += pending_whitespace + chunk
                        pending_whitespace = ""

                        now = time.monotonic()
                        if now - last_draft_at >= 1.0:
                            draft_text = full_text.strip()
                            if len(draft_text) > TELEGRAM_SAFE_MESSAGE_LENGTH:
                                draft_text = (
                                    draft_text[:TELEGRAM_SAFE_MESSAGE_LENGTH - 1].rstrip()
                                    + "…"
                                )

                            if draft_text:
                                rendered_text, entities = _render_for_telegram(draft_text)
                                try:
                                    await bot.send_message_draft(
                                        chat_id=chat_id,
                                        draft_id=draft_id,
                                        text=rendered_text,
                                        entities=entities,
                                    )
                                except TelegramError:
                                    # Drafts are best-effort and must never abort the agent.
                                    logger.warning(
                                        "Could not update Telegram draft for thread %s",
                                        thread_id,
                                        exc_info=True,
                                    )
                                finally:
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
                response_text = full_text.strip()
                if not response_text:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="A operação terminou, mas o agente não gerou uma resposta em texto.",
                    )
                    return {
                        "status": "failed",
                        "thread_id": thread_id,
                        "reason": "empty_agent_response",
                    }

                for message_part in _split_text(response_text):
                    plain_part = message_part.strip()
                    rendered_text, entities = _render_for_telegram(plain_part)
                    try:
                        await bot.send_message(
                            chat_id=chat_id,
                            text=rendered_text,
                            entities=entities,
                        )
                    except BadRequest:
                        # Invalid Markdown entities must not prevent plain-text delivery.
                        if rendered_text == plain_part and not entities:
                            raise
                        logger.warning(
                            "Formatted Telegram message was rejected; using plain text",
                            exc_info=True,
                        )
                        await bot.send_message(chat_id=chat_id, text=plain_part)

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
