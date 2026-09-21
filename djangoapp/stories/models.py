"""Domain models for the travel-story experience.

The stories feature is intentionally separated from regular blog posts. A
``Story`` represents a destination or a short visual narrative (for example,
``Koh Larn``), while ``StorySlide`` represents one ordered item inside that
narrative. ``StoryElement`` stores the text layers and affiliate call-to-action
elements rendered over each slide.

Only file paths are persisted in the database. The actual image files are
managed by Django's configured storage backend under ``MEDIA_ROOT``.
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator,  MaxValueValidator, MinValueValidator


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
    hex_color_validator = RegexValidator(
            regex=r"^#[0-9A-Fa-f]{6}$",
            message="Use uma cor no formato #RRGGBB.",
            )
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
    background_color = models.CharField(
        max_length=7,
        default="#ffffff",
        validators=[hex_color_validator],
        verbose_name="cor do fundo",
    )
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
        NONE = "none", "Sem animação"
        FADE_IN = "fade-in", "Aparecer"
        FLY_IN_BOTTOM = "fly-in-bottom", "Aparecer de baixo"
        FLY_IN_TOP = "fly-in-top", "Aparecer de cima"
        FLY_IN_LEFT = "fly-in-left", "Aparecer da esquerda"
        FLY_IN_RIGHT = "fly-in-right", "Aparecer da direita"
        SCALE_FADE_UP = "scale-fade-up", "Aparecer aumentando"
        ZOOM_IN = "zoom-in", "Aproximar"
        
    class FontWeight(models.IntegerChoices):
        THIN = 100, "Thin (100)"
        EXTRA_LIGHT = 200, "Extra Light (200)"
        LIGHT = 300, "Light (300)"
        REGULAR = 400, "Regular (400)"
        MEDIUM = 500, "Medium (500)"
        SEMI_BOLD = 600, "Semi Bold (600)"
        BOLD = 700, "Bold (700)"
        EXTRA_BOLD = 800, "Extra Bold (800)"
        BLACK = 900, "Black (900)"
    
    class FontStyle(models.TextChoices):
        NORMAL = "normal", "Normal"
        ITALIC = "italic", "Itálico"
    
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
    font_size_rem = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(Decimal("0.10")),
            MaxValueValidator(Decimal("5.00")),
        ],
        verbose_name="tamanho da fonte (rem)",
        help_text="Deixe vazio para usar o tamanho padrão.",
    )
    
    font_weight = models.PositiveSmallIntegerField(
        choices=FontWeight.choices,
        blank=True,
        null=True,
        verbose_name="peso da fonte",
        help_text="Deixe vazio para usar o peso padrão do tipo.",
    )
    
    font_style = models.CharField(
        max_length=10,
        choices=FontStyle.choices,
        default=FontStyle.NORMAL,
        verbose_name="estilo da fonte",
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
    spacing_after_rem = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("9.00")),
        ],
        verbose_name="espaço abaixo do elemento (rem)",
        help_text="Deixe vazio para usar o tamanho padrão de 0.4rem.",
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
        default=Animation.FLY_IN_BOTTOM,
        verbose_name="animação",
    )
    delay_ms = models.PositiveIntegerField(
        default=0,
        verbose_name="atraso (ms)",
        help_text="Atraso antes da animação, em milissegundos.",
    )
    duration_ms = models.PositiveIntegerField(
        default=500,
        verbose_name="duração (ms)",
        help_text="Duração da animação, em milissegundos."
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
    
    post = models.ForeignKey(
        "blog.Post",
        on_delete=models.PROTECT,
        related_name="story_elements",
        blank=True,
        null=True,
        verbose_name="post relacionado",
        help_text="Usado quando o elemento for um botão de post relacionado."
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
            has_affiliate = bool(self.affiliate_partner_id)
            has_post = bool(self.post_id)

            if not has_affiliate and not has_post:
                raise ValidationError(
                    "Escolha um parceiro afiliado ou um post."
                )

            if has_affiliate and has_post:
                raise ValidationError(
                    "Escolha somente um destino: afiliado ou post."
                )

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
