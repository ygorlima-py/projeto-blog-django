from project.celery import app

from collections.abc import Mapping
from typing import Any, cast

from rest_framework import status
from rest_framework.views import APIView, Response, Request

class TelegramAgentView(APIView):
    def post(self, request: Request) -> Response:
        
        data = cast(Mapping[str, Any], request.data)
        
        callback_query = data.get("callback_query")
        
        if callback_query:
            decision = callback_query["data"]
            thread_id = str(callback_query["from"]["id"])
            
            task = app.send_task(
                "agent.run_telegram_agent",
                kwargs={
                    "user_input": decision,
                    "thread_id": thread_id,
                    "type": "decision",
                    }
                )
            
            return Response(
                        {"task_id": task.id, "status": "queued"},
                        status=status.HTTP_202_ACCEPTED,
                    )

        message = data["message"]
        thread_id = str(data["message"]["from"]["id"])

        send_message = None
        if message.get("text"):
            send_message = message.get("text")
      
        if not send_message or not thread_id:
            return Response(
                {"detail": "user_input e thread_id são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
                )
            
        task = app.send_task(
            "agent.run_telegram_agent",
            kwargs={
                "user_input": send_message,
                "thread_id": thread_id,
                "type": "text",
                }
        )
        
        return Response(
            {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )
