import os
import uuid

import pytest
from django.core.management import call_command

from tailwind.utils import get_app_path, get_package_json_contents

from .conftest import cleanup_theme_app_dir


@pytest.mark.parametrize("legacy_version", [True, False])
def test_tailwind_install_and_build(settings, legacy_version):
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    if legacy_version:
        call_command("tailwind", "init", app_name, "--legacy")
    else:
        call_command("tailwind", "init", app_name)

    settings.INSTALLED_APPS += [app_name]

    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "apps.py")
    ), 'The "theme" app has been generated'
    call_command("tailwind", "install")

    assert os.path.isdir(
        os.path.join(get_app_path(app_name), "static_src", "node_modules")
    ), "Tailwind has been installed from npm"

    # Ensure correct version of Tailwind CSS is installed
    data = get_package_json_contents(app_name)
    tailwindcss = data.get("devDependencies", {}).get("tailwindcss", "")
    if legacy_version:
        assert tailwindcss.startswith("^1."), "Tailwind CSS v1.x is installed"
    else:
        assert tailwindcss.startswith("^2."), "Tailwind CSS v2.x is installed"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir(app_name)
