from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import strip_tags

from site_setup.validators import validate_svg


def validate_plain_text(value):
    """Reject HTML in fields intended to contain plain text only."""
    if value != strip_tags(value):
        raise ValidationError('Use somente texto, sem tags HTML.')


def validate_https_url(value):
    """Accept only complete HTTPS URLs without embedded credentials."""
    parsed_url = urlsplit(value)
    if (
        parsed_url.scheme.lower() != 'https'
        or not parsed_url.netloc
        or parsed_url.username
        or parsed_url.password
    ):
        raise ValidationError('Informe uma URL HTTPS válida.')


class AffiliateCategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def available(self):
        """Categories suitable for the public filter list."""
        return self.active().filter(partners__is_published=True).distinct()


class AffiliatePartnerQuerySet(models.QuerySet):
    def published(self):
        """Partners suitable for public pages."""
        return self.filter(is_published=True, category__is_active=True)


class AffiliateCategoryManager(models.Manager):
    def get_queryset(self):
        return AffiliateCategoryQuerySet(
            self.model,
            using=self._db,
            hints=self._hints,
        )

    def active(self):
        return self.get_queryset().active()

    def available(self):
        return self.get_queryset().available()


class AffiliatePartnerManager(models.Manager):
    def get_queryset(self):
        return AffiliatePartnerQuerySet(
            self.model,
            using=self._db,
            hints=self._hints,
        )

    def published(self):
        return self.get_queryset().published()


class AffiliateCategory(models.Model):
    name = models.CharField(max_length=60, verbose_name='nome')
    slug = models.SlugField(unique=True)
    icon = models.FileField(
        'ícone',
        upload_to='affiliates/category-icons/%Y/%m/',
        blank=True,
        validators=[validate_svg],
        help_text='Opcional. Envie um SVG seguro de até 256 KB.',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ordem')
    is_active = models.BooleanField(default=True, verbose_name='ativa')

    objects = AffiliateCategoryManager()

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'categoria de afiliado'
        verbose_name_plural = 'categorias de afiliados'

    def __str__(self):
        return self.name


class AffiliatePartner(models.Model):
    category = models.ForeignKey(
        AffiliateCategory,
        on_delete=models.PROTECT,
        related_name='partners',
        verbose_name='categoria',
    )
    name = models.CharField(max_length=100, verbose_name='nome')
    description = models.TextField(
        max_length=400,
        validators=[validate_plain_text],
        verbose_name='descrição',
    )
    image = models.ImageField(
        upload_to='affiliates/%Y/%m/',
        verbose_name='imagem',
    )
    image_alt = models.CharField(
        max_length=150,
        verbose_name='texto alternativo da imagem',
    )
    affiliate_url = models.URLField(
        max_length=1000,
        validators=[validate_https_url],
        verbose_name='link de afiliado',
    )
    button_label = models.CharField(
        max_length=40,
        default='Conhecer parceiro',
        verbose_name='texto do botão',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ordem')
    is_published = models.BooleanField(default=False, verbose_name='publicado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    objects = AffiliatePartnerManager()

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'parceiro afiliado'
        verbose_name_plural = 'parceiros afiliados'

    def __str__(self):
        return self.name
