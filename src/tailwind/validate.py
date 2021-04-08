import os

from django.apps import apps
from django.conf import settings

from .utils import get_tailwind_src_path


class ValidationError(Exception):
    pass


class Validations:
    def acceptable_label(self, label):
        if label not in [
            "init",
            "install",
            "npm",
            "start",
            "build",
            "check-updates",
            "update",
        ]:
            raise ValidationError(f"Subcommand {label} doesn't exist")

    def is_installed(self, app_name):
        if not apps.is_installed(app_name):
            raise ValidationError(f"{app_name} is not in INSTALLED_APPS")

    def is_tailwind_app(self, app_name):
        if not os.path.isfile(
            os.path.join(get_tailwind_src_path(app_name), "tailwind.config.js")
        ):
            raise ValidationError(f"'{app_name}' isn't a Tailwind app")

    def has_settings(self):
        if not hasattr(settings, "TAILWIND_APP_NAME"):
            raise ValidationError("TAILWIND_APP_NAME isn't set in settings.py")
