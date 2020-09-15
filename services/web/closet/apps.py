from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ClosetConfig(AppConfig):
    name = "closet"

    def ready(self):
        from .signals import (
            create_category_location,
            create_clothes_index,
            create_category_index,
        )

        post_migrate.connect(create_category_location, sender=self)
        post_migrate.connect(create_clothes_index, sender=self)
        post_migrate.connect(create_category_index, sender=self)
