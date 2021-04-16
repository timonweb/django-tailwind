import os
import uuid

import pytest
from django.core.management import call_command

from tailwind.utils import get_app_path

from .conftest import cleanup_theme_app_dir


@pytest.mark.parametrize("has_jit", (True, False))
def test_tailwind_install_and_build(settings, has_jit):
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    if has_jit:
        call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    else:
        call_command(
            "tailwind", "init", "--app-name", app_name, "--no-input", "--no-jit"
        )

    settings.INSTALLED_APPS += [app_name]

    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "apps.py")
    ), 'The "theme" app has been generated'

    tailwind_config_path = os.path.join(
        get_app_path(app_name), "static_src", "tailwind.config.js"
    )
    assert os.path.isfile(tailwind_config_path), "tailwind.config.js is present"

    with open(tailwind_config_path, "r") as tailwind_config:
        if has_jit:
            assert 'mode: "jit",' in tailwind_config.read()
        else:
            assert 'mode: "aot",' in tailwind_config.read()

    call_command("tailwind", "install")
    assert os.path.isdir(
        os.path.join(get_app_path(app_name), "static_src", "node_modules")
    ), "Tailwind has been installed from npm"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir(app_name)
