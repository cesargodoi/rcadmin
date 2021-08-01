from django.apps import AppConfig


class PublicworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "publicwork"

    def ready(self):
        import publicwork.signals  # noqa
