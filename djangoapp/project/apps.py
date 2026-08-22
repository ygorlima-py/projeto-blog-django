from django_summernote.apps import DjangoSummernoteConfig


class ProjectSummernoteConfig(DjangoSummernoteConfig):
    """Mantém o tipo de ID compatível com as migrations do django-summernote."""

    default_auto_field = 'django.db.models.AutoField'
