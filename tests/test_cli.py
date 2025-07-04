import os
import uuid

import pytest
from django.core.management import call_command

from tailwind.utils import get_app_path

from .conftest import cleanup_theme_app_dir


@pytest.mark.parametrize("no_package_lock", [True, False])
def test_tailwind_install_and_build_v3(no_package_lock, settings):
    """
    GIVEN a new Tailwind v3 app is initialized
    WHEN the install and build commands are run with optional package-lock settings
    THEN the app structure, dependencies, and CSS output should be created correctly
    """
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", "--app-name", app_name, "--no-input", "--tailwind-version", "3")

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), 'The "theme" app has been generated'

    tailwind_config_path = os.path.join(get_app_path(app_name), "static_src", "tailwind.config.js")
    assert os.path.isfile(tailwind_config_path), "tailwind.config.js is present"

    if no_package_lock:
        call_command("tailwind", "install", "--no-package-lock")
    else:
        call_command("tailwind", "install")

    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    assert os.path.isfile(package_json_path), "Tailwind has created package.json file"

    package_lock_json_path = os.path.join(get_app_path(app_name), "static_src", "package-lock.json")
    if no_package_lock:
        assert not os.path.isfile(package_lock_json_path), "Tailwind has not created package-lock.json file"
    else:
        assert os.path.isfile(package_lock_json_path), "Tailwind has created package-lock.json file"

    assert os.path.isdir(
        os.path.join(get_app_path(app_name), "static_src", "node_modules")
    ), "Tailwind has been installed from npm"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir(app_name)


@pytest.mark.parametrize("no_package_lock", [True, False])
def test_tailwind_install_and_build_v4(no_package_lock, settings):
    """
    GIVEN a new Tailwind v4 app is initialized
    WHEN the install and build commands are run with optional package-lock settings
    THEN the app structure, dependencies, and CSS output should be created correctly without tailwind.config.js
    """
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", "--app-name", app_name, "--no-input")

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), 'The "theme" app has been generated'

    tailwind_config_path = os.path.join(get_app_path(app_name), "static_src", "tailwind.config.js")
    assert not os.path.isfile(tailwind_config_path), "tailwind.config.js is absent from tailwind v4"

    if no_package_lock:
        call_command("tailwind", "install", "--no-package-lock")
    else:
        call_command("tailwind", "install")

    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    assert os.path.isfile(package_json_path), "Tailwind has created package.json file"

    package_lock_json_path = os.path.join(get_app_path(app_name), "static_src", "package-lock.json")
    if no_package_lock:
        assert not os.path.isfile(package_lock_json_path), "Tailwind has not created package-lock.json file"
    else:
        assert os.path.isfile(package_lock_json_path), "Tailwind has created package-lock.json file"

    assert os.path.isdir(
        os.path.join(get_app_path(app_name), "static_src", "node_modules")
    ), "Tailwind has been installed from npm"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir(app_name)
