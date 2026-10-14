from project.celery import app

from collections.abc import Mapping
from typing import Any, cast

from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.request import Request

class TelegramAgentView(APIView):
    def post(self, request: Request) -> Response:
        
        data = cast(Mapping[str, Any], request.data)
        
        
        print(data)
        # user_input = data.get("user_input")
        # thread_id = data.get("thread_id")
        
        # if not user_input or not thread_id:
        #     return Response(
        #         {"detail": "user_input e thread_id são obrigatórios"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #         )
      
        # task = app.send_task(
        #     "agent.run_telegram_agent",
        #     args=[user_input, thread_id]
        # )
        
        return Response(
            # {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )
