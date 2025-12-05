
from django.apps import AppConfig


class KnoxAllauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Knox + Allauth"

    def ready(self):
        import accounts.signals  # noqa: F401
