
from django.apps import AppConfig


class KnoxAllauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "knox_allauth"
    verbose_name = "Knox + Allauth"

    def ready(self):
        import knox_allauth.signals  # noqa: F401
