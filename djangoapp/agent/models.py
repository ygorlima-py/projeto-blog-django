from django.db import models


class ProcessedTelegramUpdate(models.Model):
    """Telegram updates already claimed for processing by the webhook."""

    update_id = models.BigIntegerField(unique=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "atualização do Telegram processada"
        verbose_name_plural = "atualizações do Telegram processadas"
