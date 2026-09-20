from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image, ImageOps
from io import BytesIO
from pathlib import Path




def resize_image(image_django, new_width=800, optimize=True, quality=60):
    image_path = (Path(settings.MEDIA_ROOT) / image_django.name).resolve()
    image_pillow = Image.open(image_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return image_pillow

    new_height = round(new_width * original_height / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS) # type: ignore

    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image

def create_square_icon(source, size=96, padding=10):
    source.open("rb")

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGBA")

        available_size = size - (padding * 2)

        resized_image = ImageOps.contain(
            image,
            (available_size, available_size),
            method=Image.Resampling.LANCZOS,
        )

        canvas = Image.new(
            "RGBA",
            (size, size),
            color=(255, 255, 255, 0),
        )

        position = (
            (size - resized_image.width) // 2,
            (size - resized_image.height) // 2,
        )

        canvas.alpha_composite(resized_image, position)

        output = BytesIO()

        canvas.save(
            output,
            format="WEBP",
            quality=85,
            method=6,
        )

    source.close()

    return ContentFile(output.getvalue())