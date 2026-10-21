from collections.abc import Mapping
from typing import Any, cast

from django.db import transaction
from project.celery import app
from rest_framework import status
from rest_framework.views import APIView, Request, Response

from .models import ProcessedTelegramUpdate


TASK_NAME = "agent.run_telegram_agent"


def _get_update_id(data: Mapping[str, Any]) -> int | None:
    raw_update_id = data.get("update_id")
    if raw_update_id is None:
        return None
    if isinstance(raw_update_id, bool):
        raise ValueError("update_id inválido")
    try:
        return int(raw_update_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("update_id inválido") from exc


def _enqueue_task_once(
    update_id: int | None,
    *,
    kwargs: dict[str, Any],
) -> tuple[Any | None, bool]:
    """Enqueue one Telegram update, atomically ignoring webhook retries."""
    if update_id is None:
        return app.send_task(TASK_NAME, kwargs=kwargs), False

    # The unique database constraint makes this safe when multiple Gunicorn
    # workers receive the same Telegram update concurrently. Keeping the task
    # publication inside the transaction also releases the claim if the broker
    # call raises, allowing Telegram to retry the update.
    with transaction.atomic():
        _, created = ProcessedTelegramUpdate.objects.get_or_create(
            update_id=update_id,
        )
        if not created:
            return None, True

        return app.send_task(TASK_NAME, kwargs=kwargs), False


class TelegramAgentView(APIView):
    def post(self, request: Request) -> Response:
        data = cast(Mapping[str, Any], request.data)

        try:
            update_id = _get_update_id(data)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        callback_query = data.get("callback_query")

        if callback_query:
            decision = callback_query["data"]
            thread_id = str(callback_query["from"]["id"])

            task, duplicate = _enqueue_task_once(
                update_id,
                kwargs={
                    "user_input": decision,
                    "thread_id": thread_id,
                    "type": "decision",
                },
            )

            if duplicate:
                return Response(
                    {"status": "duplicate"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"task_id": task.id, "status": "queued"},
                status=status.HTTP_202_ACCEPTED,
            )

        message = data["message"]
        thread_id = str(message["from"]["id"])

        send_message = message.get("text")
        if not send_message or not thread_id:
            return Response(
                {"detail": "user_input e thread_id são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task, duplicate = _enqueue_task_once(
            update_id,
            kwargs={
                "user_input": send_message,
                "thread_id": thread_id,
                "type": "text",
            },
        )

        if duplicate:
            return Response(
                {"status": "duplicate"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )
