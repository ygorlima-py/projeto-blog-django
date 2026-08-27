from urllib.parse import urlsplit

import bleach
from bleach.css_sanitizer import CSSSanitizer


TRAVELPAYOUTS_WIDGET_ATTRIBUTE = 'data-travelpayouts-src'
TRAVELPAYOUTS_WIDGET_MAX_URL_LENGTH = 4096
TRAVELPAYOUTS_WIDGET_HOSTS = frozenset({'tpemd.com'})
TRAVELPAYOUTS_WIDGET_PATHS = frozenset({'/content'})


def is_allowed_travelpayouts_widget_url(value):
    """Aceita somente o endpoint HTTPS autorizado para widgets."""
    if not isinstance(value, str):
        return False

    if (
        not value
        or len(value) > TRAVELPAYOUTS_WIDGET_MAX_URL_LENGTH
        or value != value.strip()
        or '\\' in value
        or any(ord(character) <= 31 or ord(character) == 127 for character in value)
    ):
        return False

    try:
        parsed_url = urlsplit(value)
        port = parsed_url.port
    except (UnicodeError, ValueError):
        return False

    return (
        parsed_url.scheme == 'https'
        and parsed_url.hostname in TRAVELPAYOUTS_WIDGET_HOSTS
        and parsed_url.path in TRAVELPAYOUTS_WIDGET_PATHS
        and parsed_url.username is None
        and parsed_url.password is None
        and port is None
        and not parsed_url.fragment
    )


def allow_rich_text_div_attribute(tag, name, value):
    """Preserva atributos editoriais e valida o marcador de widget."""
    if name in {'class', 'style', 'title'}:
        return True

    return (
        tag == 'div'
        and name == TRAVELPAYOUTS_WIDGET_ATTRIBUTE
        and is_allowed_travelpayouts_widget_url(value)
    )


RICH_TEXT_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'div', 'em', 'figcaption',
    'figure', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li',
    'ol', 'p', 'pre', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'th', 'thead', 'tr', 'u', 'ul',
}

RICH_TEXT_ATTRIBUTES = {
    '*': ['class', 'style', 'title'],
    'a': ['href', 'rel', 'title'],
    'div': allow_rich_text_div_attribute,
    'h1': ['id'],
    'h2': ['id'],
    'h3': ['id'],
    'h4': ['id'],
    'h5': ['id'],
    'h6': ['id'],
    'img': ['alt', 'height', 'src', 'title', 'width'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan'],
}

RICH_TEXT_CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties={
        'background-color',
        'color',
        'font-family',
        'font-size',
        'font-style',
        'font-weight',
        'line-height',
        'text-align',
        'text-decoration',
        
        
        # Imagens
        'width',
        'height',
        'max-width',
        'max-height',
        'margin',
        'margin-left',
        'margin-right',
        'display',
    },
)


def sanitize_rich_text(value):
    """Remove HTML perigoso do conteúdo produzido pelo editor rico."""
    return bleach.clean(
        value or '',
        tags=RICH_TEXT_TAGS,
        attributes=RICH_TEXT_ATTRIBUTES,
        protocols={'http', 'https', 'mailto'},
        strip=True,
        css_sanitizer=RICH_TEXT_CSS_SANITIZER,
    )


def staff_user_can_upload_rich_text_images(request):
    """Restringe anexos do Summernote aos editores do Django Admin."""
    return bool(request.user.is_authenticated and request.user.is_staff)
