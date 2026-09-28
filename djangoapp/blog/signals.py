from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from blog.models import AuthorProfile, Category


@receiver(post_save, sender=User)
def create_author_profile(sender, instance, **kwargs):
    AuthorProfile.objects.get_or_create(user=instance)

@receiver(pre_save, sender=Category)
def delete_replaced_category_cover(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous_cover_name = (
        sender.objects
        .filter(pk=instance.pk)
        .values_list("cover_image", flat=True)
        .first()
    )

    current_cover = instance.cover_image
    current_cover_name = current_cover.name if current_cover else ""

    new_file_uploaded = (
        bool(current_cover)
        and not getattr(current_cover, "_committed", True)
    )

    if previous_cover_name and (
        new_file_uploaded
        or previous_cover_name != current_cover_name
    ):
        instance.cover_image.storage.delete(previous_cover_name)


@receiver(post_delete, sender=Category)
def delete_category_cover(sender, instance, **kwargs):
    if instance.cover_image:
        instance.cover_image.delete(save=False)