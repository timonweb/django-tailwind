import json
import os

from django.apps import apps

DJANGO_TAILWIND_APP_DIR = os.path.dirname(__file__)


def get_app_path(app_name):
    app_label = app_name.split(".")[-1]
    return apps.get_app_config(app_label).path


def get_tailwind_src_path(app_name):
    return os.path.join(get_app_path(app_name), "static_src")


def get_package_json_path(app_name):
    return os.path.join(get_app_path(app_name), "static_src", "package.json")


def get_package_json_contents(app_name):
    with open(get_package_json_path(app_name), "r") as f:
        return json.load(f)


def is_path_absolute(path):
    return path.startswith("/") or path.startswith("http")


def install_pip_package(package):
    import pip._internal as pip

    pip.main(["install", package])
