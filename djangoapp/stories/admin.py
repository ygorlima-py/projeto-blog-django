from django.contrib import admin

from .models import Story, StoryElement, StorySlide
from .forms import StoryElementAdminForm, StorySlideAdminForm

class StorySlideInline(admin.TabularInline):
    """Allow slides to be created while editing a story."""

    model = StorySlide
    extra = 0
    fields = ("image", "alt_text", "order")


class StoryElementInline(admin.TabularInline):
    """Allow ordered text and CTA elements to be edited with a slide."""

    model = StoryElement
    form = StoryElementAdminForm
    extra = 0
    fields = (
        "element_type",
        "text",
        "font_size_rem",
        "font_weight",
        "font_style",
        "variant",
        "use_background_color",
        "background_color",
        "position",
        "animation",
        "delay_ms",
        "duration_ms",
        "order",
        "affiliate_partner",
        "post",
    )
    autocomplete_fields = ("affiliate_partner",)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order", "updated_at")
    list_filter = ("is_published",)
    list_editable = ("is_published", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug")
    ordering = ("order", "title")
    inlines = (StorySlideInline,)


@admin.register(StorySlide)
class StorySlideAdmin(admin.ModelAdmin):
    list_display = ("story", "order", "created_at", "updated_at")
    list_filter = ("story",)
    search_fields = ("story__title", "alt_text")
    ordering = ("story", "order", "id")
    autocomplete_fields = ("story",)
    inlines = (StoryElementInline,)
    form = StorySlideAdminForm

@admin.register(StoryElement)
class StoryElementAdmin(admin.ModelAdmin):
    list_display = (
        "slide",
        "element_type",
        "variant",
        "order",
        "affiliate_partner",
        "post",
    )
    list_filter = ("element_type", "variant", "animation")
    search_fields = ("text", "slide__story__title")
    ordering = ("slide", "order", "id")
    autocomplete_fields = ("slide", "affiliate_partner")
    form = StoryElementAdminForm
