from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
    verbose_name = 'Landing Croody'

    def ready(self) -> None:  # pragma: no cover - import por efectos secundarios
        from . import signals  # noqa: F401
        return super().ready()
