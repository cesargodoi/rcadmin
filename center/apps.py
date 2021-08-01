from django.apps import AppConfig


class CenterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "center"

    def ready(self):
        import center.signals  # noqa
