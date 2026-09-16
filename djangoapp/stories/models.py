"""Domain models for the travel-story experience.

The stories feature is intentionally separated from regular blog posts. A
``Story`` represents a destination or a short visual narrative (for example,
``Koh Larn``), while ``StorySlide`` represents one ordered item inside that
narrative. ``StoryElement`` stores the text layers and affiliate call-to-action
elements rendered over each slide.

Only file paths are persisted in the database. The actual image files are
managed by Django's configured storage backend under ``MEDIA_ROOT``.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class Story(models.Model):
    """A published or draft visual story shown on the landing page.

    ``cover`` is the image used by the story card. The story's content is
    stored in related :class:`StorySlide` instances and displayed according
    to their ``order`` value.
    """

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    cover = models.ImageField(upload_to="stories/cover/")
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "title")
        verbose_name = "story"
        verbose_name_plural = "stories"

    def save(self, *args, **kwargs):
        """Generate a stable slug when one was not supplied manually."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the human-readable story title for admin and logs."""
        return self.title


class StorySlide(models.Model):
    """One ordered image belonging to a :class:`Story`.

    ``order`` controls the sequence presented by the story viewer. Keeping
    slides in a separate model allows each story to contain any number of
    images without adding a fixed number of image fields to ``Story``.
    """

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="slides",
    )

    image = models.ImageField(upload_to="stories/slides/")
    alt_text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "slide de story"
        verbose_name_plural = "slides de story"

    def __str__(self):
        """Identify the slide by its story and display order."""
        return f"{self.story.title} — slide {self.order}"


class StoryElement(models.Model):
    """A piece of content layered over a story slide.

    A slide can contain several elements, such as a heading, a paragraph,
    a highlighted badge, or an affiliate call-to-action. The database stores
    the content and its presentation intent; CSS and JavaScript implement the
    visual style and animation.
    """
    
    hex_color_validator = RegexValidator(
        regex=r"^#[0-9A-Fa-f]{6}$",
        message="Use uma cor no formato #RRGGBB.",
        )

    class ElementType(models.TextChoices):
        TITLE = "title", "Título"
        TEXT = "text", "Texto"
        BADGE = "badge", "Destaque"
        CTA = "cta", "Botão"

    class Position(models.TextChoices):
        TOP = "top", "Superior"
        CENTER = "center", "Centro"
        BOTTOM = "bottom", "Inferior"

    class Animation(models.TextChoices):
        FADE_UP = "fade-up", "Aparecer de baixo"
        FADE = "fade", "Aparecer"
        NONE = "none", "Sem animação"
    
    slide = models.ForeignKey(
        StorySlide,
        on_delete=models.CASCADE,
        related_name="elements",
        verbose_name="slide",
    )
    element_type = models.CharField(
        max_length=20,
        choices=ElementType.choices,
        default=ElementType.TEXT,
        verbose_name="tipo",
    )
    text = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="texto",
        help_text="Texto exibido sobre a imagem. Deixe vazio para botões.",
    ) 
    variant = models.CharField(
        max_length=7,
        default="#D96C43",
        validators=[hex_color_validator],
        verbose_name="cor do texto",
    )
    background_color = models.CharField(
        max_length=7,
        blank=True,
        default="",
        validators=[hex_color_validator],
        verbose_name="cor de fundo",
    )
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.CENTER,
        verbose_name="posição",
    )
    animation = models.CharField(
        max_length=20,
        choices=Animation.choices,
        default=Animation.FADE_UP,
        verbose_name="animação",
    )
    delay_ms = models.PositiveIntegerField(
        default=0,
        verbose_name="atraso (ms)",
        help_text="Atraso antes da animação, em milissegundos.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="ordem")
    affiliate_partner = models.ForeignKey(
        "affiliates.AffiliatePartner",
        on_delete=models.PROTECT,
        related_name="story_elements",
        blank=True,
        null=True,
        verbose_name="parceiro afiliado",
        help_text="Usado quando o elemento for um botão de afiliado.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "elemento de story"
        verbose_name_plural = "elementos de story"

    def clean(self):
        """Keep affiliate actions and text elements semantically consistent."""
        super().clean()

        if self.element_type == self.ElementType.CTA:
            if not self.affiliate_partner:
                raise ValidationError({
                    "affiliate_partner": (
                        "Informe um parceiro para elementos do tipo botão."
                    ),
                })
        elif self.affiliate_partner:
            raise ValidationError({
                "affiliate_partner": (
                    "O parceiro afiliado só pode ser usado em botões."
                ),
            })

        if self.element_type != self.ElementType.CTA and not self.text.strip():
            raise ValidationError({
                "text": "Informe o texto do elemento.",
            })

    def __str__(self):
        """Identify the element by slide and display order."""
        return (
            f"{self.slide} — "
            f"{self.get_element_type_display()} #{self.order}"
        )
