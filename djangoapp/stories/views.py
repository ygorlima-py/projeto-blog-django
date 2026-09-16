from django.db.models import Prefetch
from django.views.generic import DetailView
from .models import Story, StoryElement, StorySlide

class StoryDetailView(DetailView):
    model = Story
    template_name = "stories/story_detail.html"
    context_object_name = "story"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        elements = (
            StoryElement.objects
            .select_related("affiliate_partner")
            .order_by("order", "id")
        )

        slides = (
            StorySlide.objects
            .prefetch_related(
                Prefetch("elements", queryset=elements)
            )
            .order_by("order", "id")
        )

        return (
            Story.objects
            .filter(is_published=True)
            .prefetch_related(
                Prefetch("slides", queryset=slides)
            )
        )