from typing import Any

from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from .models import Story, StoryElement, StorySlide
from affiliates.models import AffiliateCategory

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
        
class StoryListView(ListView):
    model = Story
    template_name = "stories/page_stories.html"
    context_object_name = 'stories'
    paginate_by = 8
    queryset = Story.objects.filter(is_published=True).order_by('-pk')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context["affiliate_categories"] = AffiliateCategory.objects.available()
        return context
        
        