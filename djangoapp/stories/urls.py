from django.urls import path

from .views import StoryDetailView

app_name = "stories"

urlpatterns = [
    path("<slug:slug>/", StoryDetailView.as_view(), name="detail"),
]