from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ClosetConfig(AppConfig):
    name = "closet"

    def ready(self):
        from .signals import create_default_category

        post_migrate.connect(create_default_category, sender=self)
