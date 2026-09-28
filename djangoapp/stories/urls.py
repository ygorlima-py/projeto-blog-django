from django.urls import path

from .views import StoryDetailView, StoryListView

app_name = "stories"

urlpatterns = [
    path("<slug:slug>/", StoryDetailView.as_view(), name="detail"),
    path("", StoryListView.as_view(), name="list"),
]