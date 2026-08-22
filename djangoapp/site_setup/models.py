from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image
from site_setup.validators import validate_menu_url

# Create your models here.
class MenuLink(models.Model):
    class Meta:
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

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name        

        if favicon_changed:
            resize_image(self.favicon, 32)
        

    def __str__(self):
        return self.title
