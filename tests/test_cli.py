import json
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

    # DaisyUI should NOT be present in package.json
    with open(package_json_path, "r") as f:
        package_json = json.load(f)
    assert "daisyui" not in package_json["devDependencies"], "DaisyUI dependency is NOT present in package.json"

    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    assert os.path.isfile(styles_css_path), "styles.css file exists"
    with open(styles_css_path, "r") as f:
        styles_content = f.read()
    assert '@plugin "daisyui";' not in styles_content, "DaisyUI plugin is NOT included in styles.css"

    cleanup_theme_app_dir(app_name)


def test_tailwind_init_with_daisy_ui_v4(settings):
    """
    GIVEN a new Tailwind v4 app is initialized with the --include-daisy-ui flag
    WHEN the init command is run
    THEN the DaisyUI dependency should be included in package.json and styles.css should include the plugin
    """
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", "--app-name", app_name, "--no-input", "--include-daisy-ui")

    settings.INSTALLED_APPS += [app_name]

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), 'The "theme" app has been generated'

    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    assert os.path.isfile(package_json_path), "package.json file exists"

    with open(package_json_path, "r") as f:
        package_json = json.load(f)

    assert "daisyui" in package_json["devDependencies"], "DaisyUI dependency is present in package.json"
    assert package_json["devDependencies"]["daisyui"] == "^5.0.43", "DaisyUI version is correct"

    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    assert os.path.isfile(styles_css_path), "styles.css file exists"

    with open(styles_css_path, "r") as f:
        styles_content = f.read()

    assert '@plugin "daisyui";' in styles_content, "DaisyUI plugin is included in styles.css"

    cleanup_theme_app_dir(app_name)
