import re
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from django.core.exceptions import ValidationError


MAX_SVG_SIZE = 256 * 1024
SVG_NAMESPACE = 'http://www.w3.org/2000/svg'
SAFE_SVG_ELEMENTS = {
    'svg',
    'g',
    'path',
    'circle',
    'ellipse',
    'rect',
    'line',
    'polyline',
    'polygon',
    'title',
    'desc',
    'defs',
    'clipPath',
    'mask',
    'linearGradient',
    'radialGradient',
    'stop',
}
SAFE_SVG_ATTRIBUTES = {
    'xmlns',
    'version',
    'viewBox',
    'preserveAspectRatio',
    'width',
    'height',
    'x',
    'y',
    'x1',
    'y1',
    'x2',
    'y2',
    'cx',
    'cy',
    'r',
    'rx',
    'ry',
    'd',
    'points',
    'transform',
    'opacity',
    'fill',
    'fill-opacity',
    'fill-rule',
    'stroke',
    'stroke-width',
    'stroke-linecap',
    'stroke-linejoin',
    'stroke-miterlimit',
    'stroke-opacity',
    'stroke-dasharray',
    'stroke-dashoffset',
    'clip-path',
    'clip-rule',
    'mask',
    'id',
    'class',
    'offset',
    'stop-color',
    'stop-opacity',
    'gradientUnits',
    'gradientTransform',
    'spreadMethod',
    'vector-effect',
    'shape-rendering',
    'focusable',
    'role',
    'aria-hidden',
    'aria-label',
}
SAFE_INTERNAL_REFERENCE = re.compile(r'url\(#[A-Za-z_][\w:.-]*\)')


def _xml_local_name(name):
    return name.rsplit('}', 1)[-1]


def validate_svg(uploaded_file):
    """Aceita SVGs simples e rejeita conteúdo ativo ou referências externas."""
    filename = getattr(uploaded_file, 'name', '')
    if Path(filename).suffix.lower() != '.svg':
        raise ValidationError('O ícone precisa ser um arquivo SVG.')

    current_position = uploaded_file.tell()
    uploaded_file.seek(0)
    content = uploaded_file.read(MAX_SVG_SIZE + 1)
    uploaded_file.seek(current_position)

    if len(content) > MAX_SVG_SIZE:
        raise ValidationError('O SVG deve ter no máximo 256 KB.')

    try:
        svg_text = content.decode('utf-8-sig')
    except UnicodeDecodeError as error:
        raise ValidationError('O SVG precisa usar codificação UTF-8.') from error

    lowered_svg = svg_text.lower()
    if '<!doctype' in lowered_svg or '<!entity' in lowered_svg:
        raise ValidationError('DOCTYPE e entidades não são permitidos no SVG.')

    try:
        root = ElementTree.fromstring(svg_text)
    except ElementTree.ParseError as error:
        raise ValidationError('O arquivo enviado não é um SVG válido.') from error

    if _xml_local_name(root.tag) != 'svg':
        raise ValidationError('O elemento principal do arquivo deve ser <svg>.')

    if root.tag.startswith('{'):
        namespace = root.tag[1:].split('}', 1)[0]
        if namespace != SVG_NAMESPACE:
            raise ValidationError('O arquivo usa um namespace SVG inválido.')

    for element in root.iter():
        element_name = _xml_local_name(element.tag)
        if element_name not in SAFE_SVG_ELEMENTS:
            raise ValidationError(
                f'O elemento <{element_name}> não é permitido no SVG.'
            )

        for raw_attribute, raw_value in element.attrib.items():
            attribute = _xml_local_name(raw_attribute)
            if attribute not in SAFE_SVG_ATTRIBUTES:
                raise ValidationError(
                    f'O atributo {attribute} não é permitido no SVG.'
                )

            value = raw_value.strip()
            lowered_value = value.lower()
            if any(
                blocked_value in lowered_value
                for blocked_value in ('javascript:', 'data:', '@import')
            ):
                raise ValidationError('O SVG contém uma referência insegura.')

            if 'url(' in lowered_value and (
                attribute not in {'clip-path', 'mask'}
                or not SAFE_INTERNAL_REFERENCE.fullmatch(value)
            ):
                raise ValidationError('O SVG contém uma referência externa.')


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
