from mcp_server import MCPToolset
from typing import Any, Literal
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Story, StorySlide, StoryElement


ElementType = Literal['title', 'text', 'badge', 'cta']
Position = Literal['top', 'center', 'bottom']
Animation = Literal[
                    'none', 'fade-in', 'fly-in-bottom',
                    'fly-in-top', 'fly-in-left', 'fly-in-right',
                    'scale-fade-up', 'zoom-in',
                    ]
FontWeight = Literal[100,200,300,400,500,600,700,800,900]
FontStyle = Literal['normal', 'italic']

_EDITABLE_ELEMENTS_FIELDS = {
        "slide_id",
        "element_type",
        "text",
        "font_size_rem",
        "font_weight",
        "font_style",
        "variant",
        "background_color",
        "spacing_after_rem",
        "position",
        "animation",
        "delay_ms",
        "duration_ms",
        "order",
    }

_EDITABLE_STORY_FIELDS = {
    "title",
    "slug",
}
class StoryTools(MCPToolset):
    """MCP tools for reading and editing stories and their slide elements.

    These tools expose the story editor's data model to an LLM. Read tools
    should be used to inspect the current structure before a write tool is
    called. Write tools validate model data and return a concise result that
    identifies the affected slide or element.
    """

    def list_published_stories(self) -> list[dict[str, Any]]:
        """
        Return all stories that are currently published on the site.

        Use this tool to discover the available stories before requesting the
        details of a specific story. Each item contains the story title, its
        database ID, and its creation timestamp in ISO 8601 format.

        Returns:
            A list of dictionaries with the keys ``title``, ``story_id``, and
            ``created_at``. The list is empty when no published stories exist.
        """
        stories = Story.objects.filter(is_published=True)
        
        result = [
            {
                "title": story.title,
                "story_id": story.id,
                "created_at": story.created_at.isoformat(),
            }
            for story in stories
        ]
        return result
    
    def show_story_detail_by_id(self, story_id: int) -> list[dict[str, Any]]:
        """
        Return the slides and overlay elements belonging to a story.

        This is a read-only operation. Use it before creating or editing an
        element so the LLM can inspect the current content and styles. Each
        slide includes its ``slide_id`` and image metadata. Each element
        includes its ``element_id``, content, typography, colors, spacing,
        position, animation settings, and display order.

        Use the returned ``slide_id`` when creating an element and the returned
        ``element_id`` when updating an existing element. If the story has no
        slides, this method returns an empty list.

        Args:
            story_id: The database ID of the story whose slides should be read.

        Returns:
            A list of slide dictionaries, each containing an ``elements`` list.
        """
        slides = StorySlide.objects.filter(story_id=story_id)
        
        result = [                  
            {   "slide_id": slide.id,
                "image_url": (
                    self.request.build_absolute_uri(slide.image.url)
                    if slide.image
                    else None
                ),
                "image_description": slide.alt_text,
                "background_color": slide.background_color,
                "elements": [
                    {   "element_id": element.id,
                        "element_type": element.element_type,
                        "text": element.text,
                        "font_size_rem": element.font_size_rem,
                        "font_weight": element.font_weight,
                        "font_style": element.font_style,
                        "font_color": element.variant,
                        "background_color": element.background_color,
                        "spacing_below_the_element_rem": element.spacing_after_rem,
                        "position": element.position,
                        "animation": element.animation,
                        "delay_ms_animation": element.delay_ms,
                        "duration_ms_animation": element.duration_ms,
                        "order_element":element.order,
                    }
                    for element in slide.elements.all()
                ]
            }
            for slide in slides
        ]
    
        return result

    def create_story_element(
        self,
        slide_id: int,
        element_type: ElementType,
        text: str,
        font_size_rem: float | None = None, 
        font_weight: FontWeight | None = None,
        font_style: FontStyle = "normal",
        font_color: str = "#D96C43",
        background_color: str = "",
        spacing_below_the_element_rem: float | None = None,
        position: Position = 'center',
        animation: Animation = 'none',
        delay_ms: int = 0,
        duration_ms: int = 0,
        order: int = 0,
        ) -> dict[str, Any]:
        """Create and persist a text element on an existing story slide.

        Use ``show_story_detail_by_id`` first to obtain a valid ``slide_id``
        and to understand the slide's existing layout. The element's content,
        typography, colors, spacing, position, animation, and order are
        controlled by the arguments below. The model's validation rules run
        before the element is saved.

        Args:
            slide_id: Database ID of the slide that will receive the element.
            element_type: Element kind supported by the story editor: title,
                text, badge, or cta.
            text: Text rendered inside the element.
            font_size_rem: Optional font size in rem units.
            font_weight: Optional numeric CSS font weight.
            font_style: Font style, either ``normal`` or ``italic``.
            font_color: Text color as a CSS color value.
            background_color: Element background color as a CSS color value.
                An empty string means no explicit background color.
            spacing_below_the_element_rem: Optional spacing after the element,
                expressed in rem units.
            position: Vertical placement on the slide: top, center, or bottom.
            animation: Entry animation supported by the story editor.
            delay_ms_animation: Animation delay in milliseconds.
            duration_ms_animation: Animation duration in milliseconds.
            order_element: Position used to order elements on the slide.

        Returns:
            A success dictionary containing the new element ID, or an error
            dictionary when ``slide_id`` does not identify an existing slide.

        Raises:
            ValidationError: If the element violates a model validation rule.
        """
        slide = StorySlide.objects.filter(pk=slide_id).first()
        
        if slide is None:
            return {
                "Error": f"Slide id={slide_id} not found, try with other id"
            }
            
        element = StoryElement(
            slide=slide,
            element_type=element_type,
            text=text,
            font_size_rem=(
                Decimal(str(font_size_rem))
                if font_size_rem is not None else None
            ),
            font_weight=font_weight,
            font_style=font_style,
            variant=font_color,
            background_color=background_color,
            spacing_after_rem=(
                Decimal(str(spacing_below_the_element_rem))
                if spacing_below_the_element_rem is not None else None
            ),
            position=position,
            animation=animation,
            delay_ms=delay_ms,
            duration_ms=duration_ms,
            order=order,
        )

        element.full_clean()
        element.save()
        
        return {
            "tool_response": f'Element {element.id} was created successfully on slide {slide.id} with the text: "{element.text}".'
        }
    
    @transaction.atomic
    def update_story_element(
        self,
        element_id: int,
        changes: dict[str, Any],
        ) -> dict[str, Any]:
        """
        Update an existing story element using an allowlisted set of fields.

        Use ``show_story_detail_by_id`` first to locate the correct
        ``element_id`` and inspect its current values. Only fields listed in
        the module's editable-field allowlist may be changed; arbitrary model
        attributes are rejected. The row is locked inside an atomic
        transaction, model validation runs before saving, and the response
        identifies every field that was updated.

        Args:
            element_id: Database ID of the element to update.
            changes: Mapping of editable field names to their new values.

        Returns:
            A dictionary containing the element ID, the names of the updated
            fields, and a success message.

        Raises:
            ValueError: If the element does not exist, a field is not allowed,
                or the proposed values fail model validation.
        """
        element = (
            StoryElement.objects
            .select_for_update()
            .filter(pk=element_id)
            .first()
        )
        
        if element is None:
            raise ValueError(f"Elemento {element_id} não encontrado.")
        
        unknown_fields = set(changes) - _EDITABLE_ELEMENTS_FIELDS
        if unknown_fields:
            raise ValueError(
                f"Campos não permitidos: {', '.join(sorted(unknown_fields))}"
            )
        
        
        for field, value in changes.items():
            setattr(element, field, value)
            
        try:
            element.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error
        
        element.save()
        
        return {
            "element_id": element.id,
            "updated_fields": list(changes),
            "message": f"Element {element.id} updated successfully.",
        }

    
    def update_story(self, story_id: int, changes: dict[str, Any]) -> dict[str, str | int | list]:
        """
            Update an existing story using an allowlisted set of editable fields.

            The story is identified by its primary key. Before saving, the method
            validates every requested field against the editable-field allowlist,
            applies the changes, and runs Django model validation with ``full_clean()``.

            Args:
                story_id: Database ID of the story to update.
                changes: Mapping of field names to their new values. Only fields
                    included in ``_EDITABLE_STORY_FIELDS`` may be changed.

            Returns:
                A dictionary containing the updated story ID, the list of updated
                fields, and a success message.

            Raises:
                ValueError: If the story does not exist, an unknown field is provided,
                    or the updated values fail model validation.
        """
        
        story = Story.objects.filter(pk=story_id).first()
        
        if story is None:
            raise ValueError(f"Elemento {story_id} não encontrado.")
                
        unknown_fields = set(changes) - _EDITABLE_STORY_FIELDS
        if unknown_fields:
            raise ValueError(
                f"Campos não permitidos: {', '.join(sorted(unknown_fields))}"
            )
        for field, value in changes.items():
            setattr(story, field, value)

        try:
            story.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error
        
        story.save()
        
        return {
            "element_id": story.id,
            "updated_fields": list(changes),
            "message": f"Element {story.id} updated successfully.",
        }