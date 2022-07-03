import os
import uuid

from django.core.management import call_command

from django_tailwind.utils import get_app_path

from .conftest import cleanup_theme_app_dir


def test_tailwind_install_and_build(settings):
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", "--app-name", app_name, "--no-input")

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), 'The "theme" app has been generated'

    tailwind_config_path = os.path.join(get_app_path(app_name), "static_src", "tailwind.config.js")
    assert os.path.isfile(tailwind_config_path), "tailwind.config.js is present"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir(app_name)
