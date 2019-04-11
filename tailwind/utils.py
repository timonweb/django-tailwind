import os

from django.apps import apps

DJANGO_TAILWIND_APP_DIR = os.path.dirname(__file__)


def get_app_path(app_name):
    return apps.get_app_config(app_name).path


def get_tailwind_src_path(app_name):
    return os.path.join(get_app_path(app_name), "static_src")
