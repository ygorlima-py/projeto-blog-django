import base64
import binascii
from decimal import Decimal
from io import BytesIO
from pathlib import PurePath
from typing import Any, Literal

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from mcp_server import MCPToolset
from PIL import Image, UnidentifiedImageError

from blog.models import Post
from .models import AffiliateLink, Story, StorySlide, StoryElement


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
    "font_color",
    "background_color",
    "spacing_below_the_element_rem",
    "position",
    "animation",
    "delay_ms",
    "duration_ms",
    "order",
    "affiliate_link_id",
    "post_id",
}

_ELEMENT_API_TO_MODEL_FIELDS = {
    "font_color": "variant",
    "spacing_below_the_element_rem": "spacing_after_rem",
}

_EDITABLE_STORY_FIELDS = {
    "title",
    "slug",
    "order",
    "cover",
}

_MAX_STORY_SLIDE_IMAGE_BYTES = 10 * 1024 * 1024


def _decode_story_image(
    image_base64: str,
    filename: str,
) -> tuple[bytes, str]:
    """Decode and validate an image received by a story-slide tool."""
    safe_filename = PurePath(filename.replace("\\", "/")).name
    if not safe_filename or safe_filename in {".", ".."}:
        raise ValueError("filename deve conter um nome de arquivo válido.")

    payload = image_base64.strip()
    if "," in payload and payload.lower().startswith("data:"):
        payload = payload.split(",", 1)[1]
    payload = "".join(payload.split())

    try:
        image_bytes = base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("image_base64 não contém um Base64 válido.") from error

    if not image_bytes:
        raise ValueError("A imagem enviada está vazia.")
    if len(image_bytes) > _MAX_STORY_SLIDE_IMAGE_BYTES:
        raise ValueError("A imagem não pode exceder 10 MB.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("O conteúdo enviado não é uma imagem válida.") from error

    return image_bytes, safe_filename



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
        stories = Story.objects.filter(is_published=True).order_by("order")
        
        result = [
            {
                "title": story.title,
                "story_id": story.id,
                "order": story.order,
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
        slides = (
            StorySlide.objects
            .filter(story_id=story_id)
            .prefetch_related(
                "elements__affiliate_link__affiliate_partner",
                "elements__post",
            )
            .order_by("order")
        )
        
        result = [                  
            {   "slide_id": slide.id,
                "order": slide.order,
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
                        "delay_ms": element.delay_ms,
                        "duration_ms": element.duration_ms,
                        "order": element.order,
                        "affiliate_link_id": element.affiliate_link_id,
                        "affiliate_link_name": (
                            element.affiliate_link.name
                            if element.affiliate_link_id else None
                        ),
                        "affiliate_link_url": (
                            element.affiliate_link.url
                            if element.affiliate_link_id else None
                        ),
                        "post_id": element.post_id,
                        "post_title": element.post.title if element.post else None,
                    }
                    for element in slide.elements.all()
                ]
            }
            for slide in slides
        ]
    
        return result

    @transaction.atomic
    def create_story(
        self,
        title: str,
        cover_base64: str,
        cover_filename: str,
        slug: str | None = None,
        order: int = 0,
    ) -> dict[str, Any]:
        """Create a new unpublished story with a cover image.

        The story is always created as a draft. Publishing remains an admin
        responsibility, so ``is_published`` is intentionally not exposed as
        an argument of this tool.

        Args:
            title: Human-readable story title.
            cover_base64: Cover image encoded as Base64 or a data URI.
            cover_filename: Filename for the cover image.
            slug: Optional unique URL slug. If omitted, Django generates it
                from the title.
            order: Position of the story in the published story list.

        Returns:
            The created story ID, title, slug, cover URL, and order.

        Raises:
            ValueError: If the title or cover data is invalid, or the slug is
                already in use.
        """
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("title não pode ficar vazio.")

        image_bytes, safe_filename = _decode_story_image(
            cover_base64,
            cover_filename,
        )

        story = Story(
            title=clean_title,
            slug=slug.strip() if slug is not None else "",
            is_published=False,
            order=order,
        )
        story.cover = ContentFile(image_bytes, name=safe_filename)

        try:
            story.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error

        story.save()

        cover_url = story.cover.url
        if getattr(self, "request", None) is not None:
            cover_url = self.request.build_absolute_uri(cover_url)

        return {
            "story_id": story.id,
            "title": story.title,
            "slug": story.slug,
            "cover_url": cover_url,
            "order": story.order,
            "message": f"Story {story.id} created successfully.",
        }

    @transaction.atomic
    def create_story_slide(
        self,
        story_id: int,
        image_base64: str,
        filename: str,
        alt_text: str,
        order: int = 0,
        background_color: str = "#ffffff",
    ) -> dict[str, Any]:
        """Create a story slide with an uploaded image.

        The image must be provided as raw Base64 or as a data URI such as
        ``data:image/jpeg;base64,...``. The image is validated by Django's
        ``ImageField`` before it is persisted.

        Args:
            story_id: Database ID of the story that will receive the slide.
            image_base64: Image bytes encoded as Base64, optionally prefixed
                with a data URI header.
            filename: Original image filename. Only its final path component
                is used when saving the file.
            alt_text: Accessible description of the image, up to 150 chars.
            order: Position of the slide in the story.
            background_color: Slide background color in ``#RRGGBB`` format.

        Returns:
            The created slide ID, image URL, and saved slide metadata.

        Raises:
            ValueError: If the story does not exist, the Base64 data is
                invalid or too large, or the supplied metadata is invalid.
            ValidationError: If the uploaded file or slide data fails model
                validation.
        """
        story = Story.objects.filter(pk=story_id).first()
        if story is None:
            raise ValueError(f"Story id={story_id} não encontrado.")

        clean_alt_text = alt_text.strip()
        if not clean_alt_text:
            raise ValueError("alt_text não pode ficar vazio.")
        if len(clean_alt_text) > 150:
            raise ValueError("alt_text deve ter no máximo 150 caracteres.")

        image_bytes, safe_filename = _decode_story_image(
            image_base64,
            filename,
        )

        slide = StorySlide(
            story=story,
            alt_text=clean_alt_text,
            order=order,
            background_color=background_color,
        )
        slide.image = ContentFile(image_bytes, name=safe_filename)
        slide.full_clean()
        slide.save()

        image_url = slide.image.url
        if getattr(self, "request", None) is not None:
            image_url = self.request.build_absolute_uri(image_url)

        return {
            "slide_id": slide.id,
            "story_id": story.id,
            "image_url": image_url,
            "alt_text": slide.alt_text,
            "order": slide.order,
            "message": f"Slide {slide.id} created successfully on story {story.id}.",
        }


    @transaction.atomic
    def update_story_slide(
        self,
        slide_id: int,
        image_base64: str | None = None,
        filename: str | None = None,
        alt_text: str | None = None,
        order: int | None = None,
        background_color: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing story slide using only supplied fields.

        Use ``show_story_detail_by_id`` first to locate the correct
        ``slide_id``. When replacing the image, provide both ``image_base64``
        and ``filename``. The image accepts raw Base64 or a data URI and is
        validated before being saved.

        Args:
            slide_id: Database ID of the slide to update.
            image_base64: Optional replacement image encoded as Base64.
            filename: Filename for the replacement image.
            alt_text: Optional accessible image description, up to 150 chars.
            order: Optional position of the slide in the story.
            background_color: Optional slide background color in ``#RRGGBB``.

        Returns:
            The updated slide ID, image URL, metadata, and field names.

        Raises:
            ValueError: If the slide does not exist, no fields were supplied,
                the image input is incomplete, or the image is invalid.
            ValidationError: If the updated slide fails model validation.
        """
        slide = (
            StorySlide.objects
            .select_for_update()
            .filter(pk=slide_id)
            .first()
        )
        if slide is None:
            raise ValueError(f"Slide id={slide_id} não encontrado.")

        changes: list[str] = []

        if image_base64 is not None:
            if not filename:
                raise ValueError(
                    "filename é obrigatório quando a imagem é atualizada."
                )
            image_bytes, safe_filename = _decode_story_image(
                image_base64,
                filename,
            )
            slide.image = ContentFile(image_bytes, name=safe_filename)
            changes.append("image")
        elif filename is not None:
            raise ValueError(
                "image_base64 é obrigatório quando filename é informado."
            )

        if alt_text is not None:
            clean_alt_text = alt_text.strip()
            if not clean_alt_text:
                raise ValueError("alt_text não pode ficar vazio.")
            if len(clean_alt_text) > 150:
                raise ValueError("alt_text deve ter no máximo 150 caracteres.")
            slide.alt_text = clean_alt_text
            changes.append("alt_text")

        if order is not None:
            slide.order = order
            changes.append("order")

        if background_color is not None:
            slide.background_color = background_color
            changes.append("background_color")

        if not changes:
            raise ValueError("Informe ao menos um campo para atualizar.")

        slide.full_clean()
        slide.save()

        image_url = slide.image.url if slide.image else None
        if image_url and getattr(self, "request", None) is not None:
            image_url = self.request.build_absolute_uri(image_url)

        return {
            "slide_id": slide.id,
            "story_id": slide.story_id,
            "image_url": image_url,
            "alt_text": slide.alt_text,
            "order": slide.order,
            "background_color": slide.background_color,
            "updated_fields": changes,
            "message": f"Slide {slide.id} updated successfully.",
        }


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
        affiliate_link_id: int | None = None,
        post_id: int | None = None,
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
            delay_ms: Animation delay in milliseconds.
            duration_ms: Animation duration in milliseconds.
            order: Position used to order elements on the slide.
            affiliate_link_id: Optional ID of the affiliate link used by a CTA.
            post_id: Optional ID of the related post used by a CTA.

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
            
        affiliate_link = None
        if affiliate_link_id is not None:
            affiliate_link = (
                AffiliateLink.objects
                .select_related("affiliate_partner")
                .filter(pk=affiliate_link_id)
                .first()
            )
            if affiliate_link is None:
                raise ValueError(
                    f"Link afiliado id={affiliate_link_id} não encontrado."
                )

        post = None
        if post_id is not None:
            post = Post.objects.filter(pk=post_id).first()
            if post is None:
                raise ValueError(f"Post id={post_id} não encontrado.")

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
            affiliate_link=affiliate_link,
            post=post,
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
                Use ``affiliate_link_id`` to associate a CTA with an
                affiliate link, or ``None`` to remove that association.
                Use ``post_id`` to associate a CTA with a related post, or
                ``None`` to remove that association.

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
        
        changes = dict(changes)
        affiliate_link_id_provided = "affiliate_link_id" in changes
        affiliate_link_id = changes.pop("affiliate_link_id", None)
        post_id_provided = "post_id" in changes
        post_id = changes.pop("post_id", None)

        unknown_fields = set(changes) - _EDITABLE_ELEMENTS_FIELDS
        if unknown_fields:
            raise ValueError(
                f"Campos não permitidos: {', '.join(sorted(unknown_fields))}"
            )

        updated_fields = []
        if affiliate_link_id_provided:
            affiliate_link = None
            if affiliate_link_id is not None:
                affiliate_link = (
                    AffiliateLink.objects
                    .select_related("affiliate_partner")
                    .filter(pk=affiliate_link_id)
                    .first()
                )
                if affiliate_link is None:
                    raise ValueError(
                        f"Link afiliado id={affiliate_link_id} não encontrado."
                    )
            element.affiliate_link = affiliate_link
            updated_fields.append("affiliate_link_id")

        if post_id_provided:
            post = None
            if post_id is not None:
                post = Post.objects.filter(pk=post_id).first()
                if post is None:
                    raise ValueError(f"Post id={post_id} não encontrado.")
            element.post = post
            updated_fields.append("post_id")

        for field, value in changes.items():
            model_field = _ELEMENT_API_TO_MODEL_FIELDS.get(field, field)
            setattr(element, model_field, value)
        updated_fields.extend(changes)
            
        try:
            element.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error
        
        element.save()
        
        return {
            "element_id": element.id,
            "updated_fields": updated_fields,
            "message": f"Element {element.id} updated successfully.",
        }
    
    @transaction.atomic
    def update_story(
        self,
        story_id: int,
        changes: dict[str, Any],
        cover_base64: str | None = None,
        cover_filename: str | None = None,
    ) -> dict[str, str | int | list]:
        """Update an existing story's editable content and cover image.

        The editable story fields are ``title``, ``slug`` and ``order``.
        ``is_published`` is intentionally not editable here; publication is
        controlled through the Django admin. To replace the cover image,
        provide both ``cover_base64`` and ``cover_filename``. The image uses
        the same Base64/data-URI validation as story slides.

        Args:
            story_id: Database ID of the story to update.
            changes: Mapping containing optional ``title``, ``slug`` and
                ``order`` values.
            cover_base64: Optional replacement cover encoded as Base64 or a
                data URI.
            cover_filename: Filename for the replacement cover image.

        Returns:
            A dictionary containing the updated story ID, fields, cover URL,
            and a success message.

        Raises:
            ValueError: If the story does not exist, an unknown field is
                supplied, the cover arguments are incomplete, or the image is
                invalid.
        """
        story = (
            Story.objects
            .select_for_update()
            .filter(pk=story_id)
            .first()
        )

        if story is None:
            raise ValueError(f"Story id={story_id} não encontrado.")

        unknown_fields = set(changes) - _EDITABLE_STORY_FIELDS
        if unknown_fields:
            raise ValueError(
                f"Campos não permitidos: {', '.join(sorted(unknown_fields))}"
            )

        updated_fields = list(changes)
        for field, value in changes.items():
            setattr(story, field, value)

        if cover_base64 is not None:
            if not cover_filename:
                raise ValueError(
                    "cover_filename é obrigatório quando o cover é atualizado."
                )
            image_bytes, safe_filename = _decode_story_image(
                cover_base64,
                cover_filename,
            )
            story.cover = ContentFile(image_bytes, name=safe_filename)
            updated_fields.append("cover")
        elif cover_filename is not None:
            raise ValueError(
                "cover_base64 é obrigatório quando cover_filename é informado."
            )

        if not updated_fields:
            raise ValueError("Informe ao menos um campo para atualizar.")

        try:
            story.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error

        story.save()

        cover_url = story.cover.url if story.cover else None
        if cover_url and getattr(self, "request", None) is not None:
            cover_url = self.request.build_absolute_uri(cover_url)

        return {
            "story_id": story.id,
            "updated_fields": updated_fields,
            "cover_url": cover_url,
            "message": f"Story {story.id} updated successfully.",
        }
