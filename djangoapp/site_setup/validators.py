from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_menu_url(value):
    """Permite apenas caminhos internos, âncoras ou URLs HTTPS no menu."""
    if (
        value.startswith('/')
        and not value.startswith('//')
        and '\\' not in value
    ):
        return

    if value.startswith('#'):
        return

    parsed_url = urlparse(value)
    if parsed_url.scheme == 'https' and parsed_url.netloc:
        return

    raise ValidationError(
        'Use um caminho interno iniciado por /, uma âncora # ou uma URL HTTPS.'
    )
