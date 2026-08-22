import bleach
from bleach.css_sanitizer import CSSSanitizer
from django.db import migrations


RICH_TEXT_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'div', 'em', 'figcaption',
    'figure', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li',
    'ol', 'p', 'pre', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'th', 'thead', 'tr', 'u', 'ul',
}

RICH_TEXT_ATTRIBUTES = {
    '*': ['class', 'style', 'title'],
    'a': ['href', 'rel', 'title'],
    'img': ['alt', 'height', 'src', 'title', 'width'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan'],
}

RICH_TEXT_CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties={
        'background-color', 'color', 'font-family', 'font-size', 'font-style',
        'font-weight', 'line-height', 'text-align', 'text-decoration',
    },
)


def sanitize_content(value):
    return bleach.clean(
        value or '',
        tags=RICH_TEXT_TAGS,
        attributes=RICH_TEXT_ATTRIBUTES,
        protocols={'http', 'https', 'mailto'},
        strip=True,
        css_sanitizer=RICH_TEXT_CSS_SANITIZER,
    )


def sanitize_existing_content(apps, schema_editor):
    for model_name in ('Post', 'Page'):
        model = apps.get_model('blog', model_name)
        for item in model.objects.exclude(content='').iterator():
            cleaned_content = sanitize_content(item.content)
            if cleaned_content != item.content:
                model.objects.filter(pk=item.pk).update(content=cleaned_content)


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0012_post_is_featured_authorprofile'),
    ]

    operations = [
        migrations.RunPython(sanitize_existing_content, migrations.RunPython.noop),
    ]
