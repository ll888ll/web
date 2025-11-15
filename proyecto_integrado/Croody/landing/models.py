from __future__ import annotations

import secrets

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def _generate_ingest_token() -> str:
    return secrets.token_hex(16)


class UserProfile(models.Model):
    THEME_CHOICES = (
        ("system", _("Sistema")),
        ("dark", _("Oscuro")),
        ("light", _("Claro")),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=10, default="es")
    preferred_theme = models.CharField(max_length=12, choices=THEME_CHOICES, default="system")
    timezone = models.CharField(max_length=64, default="UTC")
    notification_level = models.CharField(max_length=24, default="smart")
    telemetry_alerts = models.BooleanField(default=True)
    ingest_token = models.CharField(max_length=64, unique=True, editable=False, default=_generate_ingest_token)
    favorite_robot = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self) -> str:  # pragma: no cover - representación legible
        return f"Perfil {self.user.get_username()}"

    def regenerate_token(self) -> None:
        self.ingest_token = _generate_ingest_token()
        self.save(update_fields=["ingest_token"])
