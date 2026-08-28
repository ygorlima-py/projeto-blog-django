from django.core.exceptions import ValidationError
from django.db import models

from utils.model_validators import validate_png
from utils.images import resize_image
from site_setup.validators import validate_menu_url


class FooterSection(models.Model):
    site_setup = models.ForeignKey(
        'SiteSetup',
        on_delete=models.CASCADE,
        related_name='footer_sections',
    )
    title = models.CharField('Título', max_length=50)
    order = models.PositiveSmallIntegerField(
        'Ordem',
        default=0,
        help_text='Números menores aparecem primeiro.',
    )

    class Meta:
        ordering = ('order', 'pk')
        verbose_name = 'Categoria do rodapé'
        verbose_name_plural = 'Categorias do rodapé'
        constraints = (
            models.UniqueConstraint(
                fields=('site_setup', 'title'),
                name='unique_footer_section_title_per_site',
            ),
        )

    def __str__(self):
        return self.title


# Create your models here.
class MenuLink(models.Model):
    class Meta:
        ordering = ('order', 'pk')
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    class Placement(models.TextChoices):
        BOTH = 'both', 'Cabeçalho e rodapé'
        HEADER = 'header', 'Somente cabeçalho'
        FOOTER = 'footer', 'Somente rodapé'

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=255, validators=[validate_menu_url])
    new_tab = models.BooleanField(default=False)
    placement = models.CharField(
        'Exibir em',
        max_length=6,
        choices=Placement.choices,
        default=Placement.BOTH,
    )
    order = models.PositiveSmallIntegerField(
        'Ordem',
        default=0,
        help_text='Números menores aparecem primeiro.',
    )
    footer_section = models.ForeignKey(
        FooterSection,
        on_delete=models.SET_NULL,
        related_name='links',
        blank=True,
        null=True,
        verbose_name='Categoria do rodapé',
        help_text='Opcional. Links sem categoria aparecem em Explore.',
    )
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE,
        blank=True, null=True, default=None,
        related_name='menu'
    )

    @property
    def show_in_header(self):
        return self.placement in {self.Placement.BOTH, self.Placement.HEADER}

    @property
    def show_in_footer(self):
        return self.placement in {self.Placement.BOTH, self.Placement.FOOTER}

    def clean(self):
        super().clean()
        if (
            self.footer_section_id
            and self.site_setup_id
            and self.footer_section.site_setup_id != self.site_setup_id
        ):
            raise ValidationError({
                'footer_section': 'Escolha uma categoria deste mesmo Setup.',
            })

    def __str__(self):
        return self.text


class SocialLink(models.Model):
    class Platform(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        YOUTUBE = 'youtube', 'YouTube'
        TIKTOK = 'tiktok', 'TikTok'
        FACEBOOK = 'facebook', 'Facebook'
        LINKEDIN = 'linkedin', 'LinkedIn'
        GITHUB = 'github', 'GitHub'
        X = 'x-twitter', 'X / Twitter'
        OTHER = 'link', 'Outro'

    site_setup = models.ForeignKey(
        'SiteSetup',
        on_delete=models.CASCADE,
        related_name='social_links',
    )
    platform = models.CharField(
        max_length=20,
        choices=Platform.choices,
        default=Platform.INSTAGRAM,
    )
    label = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=255)
    new_tab = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('order', 'pk')
        verbose_name = 'Link social'
        verbose_name_plural = 'Links sociais'

    @property
    def display_name(self):
        return self.label or self.get_platform_display()

    @property
    def icon_class(self):
        icons = {
            self.Platform.INSTAGRAM: 'fa-brands fa-instagram',
            self.Platform.YOUTUBE: 'fa-brands fa-youtube',
            self.Platform.TIKTOK: 'fa-brands fa-tiktok',
            self.Platform.FACEBOOK: 'fa-brands fa-facebook',
            self.Platform.LINKEDIN: 'fa-brands fa-linkedin',
            self.Platform.GITHUB: 'fa-brands fa-github',
            self.Platform.X: 'fa-brands fa-x-twitter',
            self.Platform.OTHER: 'fa-solid fa-link',
        }
        return icons[self.platform]

    def __str__(self):
        return self.display_name
    
class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True, 
        default='',
        validators=[validate_png],
    )

    logo = models.ImageField(
        'Logo do site',
        upload_to='assets/logo/%Y/%m/',
        blank=True,
        default='',
        help_text='Envie o logo completo em PNG, de preferência com fundo transparente.',
        validators=[validate_png],
    )

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        current_logo_name = str(self.logo.name)
        super().save(*args, **kwargs)
        favicon_changed = False
        logo_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if self.logo:
            logo_changed = current_logo_name != self.logo.name

        if favicon_changed:
            resize_image(self.favicon, 32)

        if logo_changed:
            resize_image(self.logo, 600)
        

    def __str__(self):
        return self.title
