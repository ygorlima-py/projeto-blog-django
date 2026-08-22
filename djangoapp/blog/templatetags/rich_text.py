from django import template
from django.utils.safestring import mark_safe

from blog.security import sanitize_rich_text


register = template.Library()


@register.filter(is_safe=True)
def rich_text(value):
    """Renderiza conteúdo editorial já higienizado, inclusive dados legados."""
    return mark_safe(sanitize_rich_text(value))
