from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import ProcessedTelegramUpdate
from .views import TelegramAgentView


class TelegramAgentWebhookTests(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = TelegramAgentView.as_view()

    @patch("agent.views.app.send_task")
    def test_same_update_is_enqueued_once(self, send_task) -> None:
        send_task.return_value.id = "task-1"
        payload = {
            "update_id": 123,
            "message": {"from": {"id": 42}, "text": "oi"},
        }

        first = self.view(
            self.factory.post("/agent/telegram/", payload, format="json")
        )
        second = self.view(
            self.factory.post("/agent/telegram/", payload, format="json")
        )

        self.assertEqual(first.status_code, 202)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.data, {"status": "duplicate"})
        self.assertEqual(send_task.call_count, 1)
        self.assertEqual(
            ProcessedTelegramUpdate.objects.filter(update_id=123).count(),
            1,
        )

    @patch("agent.views.app.send_task")
    def test_manual_payload_without_update_id_still_queues(self, send_task) -> None:
        send_task.return_value.id = "task-2"
        payload = {"message": {"from": {"id": 42}, "text": "teste"}}

        response = self.view(
            self.factory.post("/agent/telegram/", payload, format="json")
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(
            response.data,
            {"task_id": "task-2", "status": "queued"},
        )
        send_task.assert_called_once()
