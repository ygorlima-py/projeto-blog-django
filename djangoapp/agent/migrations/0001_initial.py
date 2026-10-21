from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProcessedTelegramUpdate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("update_id", models.BigIntegerField(unique=True)),
                ("received_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "atualização do Telegram processada",
                "verbose_name_plural": "atualizações do Telegram processadas",
            },
        ),
    ]
