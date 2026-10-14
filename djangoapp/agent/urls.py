from django.urls import path

from .views import TelegramAgentView

urlpatterns = [
    path("telegram/", TelegramAgentView.as_view()),
]
