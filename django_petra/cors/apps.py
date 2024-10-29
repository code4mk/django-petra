from __future__ import annotations

from django.apps import AppConfig
from django.core.checks import register
from django.core.checks import Tags

from drf_friend.cors.checks import check_settings


class CorsAppConfig(AppConfig):
    name = 'drf_friend.cors'

    def ready(self) -> None:
        register(Tags.security)(check_settings)