from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import StorySlide


@receiver(post_delete, sender=StorySlide)
def delete_story_slide_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)