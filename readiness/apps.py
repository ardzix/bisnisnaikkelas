from django.apps import AppConfig


class ReadinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'readiness'
    verbose_name = 'Readiness Assessment'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import readiness.signals  # noqa 