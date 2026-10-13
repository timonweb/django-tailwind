from django.apps import AppConfig


class TailwindConfig(AppConfig):
    name = "tailwind"

    def ready(self):
        from . import checks  # noqa: F401  (registers system checks)
