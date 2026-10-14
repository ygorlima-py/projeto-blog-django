import os

from celery import Celery
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "project.settings",
)

app = Celery(
    "django",
    broker=settings.AGENT_BROKER_URL,
    )

if __name__ == "__main__":
    result = app.send_task(
        "agent.run_telegram_agent",
        args=[
            "Mensagem de teste enviada pelo Django",
            "thread-teste"
        ],
    )
    
    print(result.id)