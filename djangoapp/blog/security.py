import bleach
from bleach.css_sanitizer import CSSSanitizer


RICH_TEXT_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'div', 'em', 'figcaption',
    'figure', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li',
    'ol', 'p', 'pre', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'th', 'thead', 'tr', 'u', 'ul',
}

RICH_TEXT_ATTRIBUTES = {
    '*': ['class', 'style', 'title'],
    'a': ['href', 'rel', 'title'],
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
