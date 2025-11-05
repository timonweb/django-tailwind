import json
import os

import pytest
from django.core.management import call_command
from django.core.management import CommandError

from tailwind.utils import get_app_path


@pytest.mark.parametrize("no_package_lock", [True, False])
def test_tailwind_install_and_build_v3(no_package_lock, settings, app_name):
    """
    GIVEN a new Tailwind v3 app is initialized
    WHEN the install and build commands are run with optional package-lock settings
    THEN the app structure, dependencies, and CSS output should be created correctly
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--no-input", "--tailwind-version", "3"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), (
        'The "theme" app has been generated'
    )

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
        assert not os.path.isfile(package_lock_json_path), (
            "Tailwind has not created package-lock.json file"
        )
    else:
        assert os.path.isfile(package_lock_json_path), "Tailwind has created package-lock.json file"

    assert os.path.isdir(os.path.join(get_app_path(app_name), "static_src", "node_modules")), (
        "Tailwind has been installed from npm"
    )

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"


@pytest.mark.parametrize("no_package_lock", [True, False])
def test_tailwind_install_and_build_v4(no_package_lock, settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized
    WHEN the install and build commands are run with optional package-lock settings
    THEN the app structure, dependencies, and CSS output should be created correctly without tailwind.config.js
    """
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        "4",
        "--no-input",
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), (
        'The "theme" app has been generated'
    )

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
        assert not os.path.isfile(package_lock_json_path), (
            "Tailwind has not created package-lock.json file"
        )
    else:
        assert os.path.isfile(package_lock_json_path), "Tailwind has created package-lock.json file"

    assert os.path.isdir(os.path.join(get_app_path(app_name), "static_src", "node_modules")), (
        "Tailwind has been installed from npm"
    )

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    # DaisyUI should NOT be present in package.json
    with open(package_json_path) as f:
        package_json = json.load(f)
    assert "daisyui" not in package_json["devDependencies"], (
        "DaisyUI dependency is NOT present in package.json"
    )

    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    assert os.path.isfile(styles_css_path), "styles.css file exists"
    with open(styles_css_path) as f:
        styles_content = f.read()
    assert '@plugin "daisyui";' not in styles_content, (
        "DaisyUI plugin is NOT included in styles.css"
    )

    # Check that DaisyUI markup is NOT present in base.html
    base_html_path = os.path.join(get_app_path(app_name), "templates", "base.html")
    assert os.path.isfile(base_html_path), "base.html file exists"
    with open(base_html_path) as f:
        base_html_content = f.read()
    assert "toast toast-top toast-end" not in base_html_content, (
        "DaisyUI toast markup is NOT present in base.html"
    )
    assert "alert alert-info" not in base_html_content, (
        "DaisyUI alert markup is NOT present in base.html"
    )
    assert "Hello from daisyUi" not in base_html_content, (
        "DaisyUI greeting text is NOT present in base.html"
    )


def test_tailwind_install_and_build_v4_standalone(settings, app_name):
    """
    GIVEN a new Tailwind v4s (standalone) app is initialized
    WHEN the install and build commands are run
    THEN the app structure should be created correctly
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--no-input", "--tailwind-version", "4s"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), (
        'The "theme" app has been generated'
    )

    call_command("tailwind", "install")

    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    assert not os.path.isfile(package_json_path), "Tailwind has not created package.json file"

    assert not os.path.isdir(os.path.join(get_app_path(app_name), "static_src", "node_modules")), (
        "Tailwind has not been installed from npm"
    )

    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    assert os.path.isfile(styles_css_path), "styles.css file exists"
    with open(styles_css_path) as f:
        styles_content = f.read()
    assert '@plugin "daisyui";' not in styles_content, (
        "DaisyUI plugin is NOT included in styles.css"
    )

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path(app_name), "static", "css", "dist", "styles.css")
    ), "Tailwind has built a css/styles.css file"


def test_tailwind_non_standalone_commands_v4_standalone(settings, app_name):
    """
    GIVEN a new Tailwind v4 standalone app is initialized
    WHEN non-standalone-specific commands are run
    THEN they should raise CommandError indicating they are not supported
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--no-input", "--tailwind-version", "4s"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    call_command("tailwind", "install")

    with pytest.raises(CommandError):
        call_command("tailwind", "update")

    with pytest.raises(CommandError):
        call_command("tailwind", "plugin_install", "some-plugin")


def test_tailwind_init_with_daisy_ui_v4(settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized with the --include-daisy-ui flag
    WHEN the init command is run
    THEN the DaisyUI dependency should be included in package.json and styles.css should include the plugin
    """
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        "4",
        "--no-input",
        "--include-daisy-ui",
    )

    settings.INSTALLED_APPS += [app_name]

    assert os.path.isfile(os.path.join(get_app_path(app_name), "apps.py")), (
        'The "theme" app has been generated'
    )

    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    assert os.path.isfile(package_json_path), "package.json file exists"

    with open(package_json_path) as f:
        package_json = json.load(f)

    assert "daisyui" in package_json["devDependencies"], (
        "DaisyUI dependency is present in package.json"
    )

    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    assert os.path.isfile(styles_css_path), "styles.css file exists"

    with open(styles_css_path) as f:
        styles_content = f.read()

    assert '@plugin "daisyui";' in styles_content, "DaisyUI plugin is included in styles.css"

    # Check that DaisyUI markup is present in base.html
    base_html_path = os.path.join(get_app_path(app_name), "templates", "base.html")
    assert os.path.isfile(base_html_path), "base.html file exists"
    with open(base_html_path) as f:
        base_html_content = f.read()
    assert "toast toast-top toast-end" in base_html_content, (
        "DaisyUI toast markup is present in base.html"
    )
    assert "alert alert-info" in base_html_content, "DaisyUI alert markup is present in base.html"
    assert "Hello from daisyUi" in base_html_content, (
        "DaisyUI greeting text is present in base.html"
    )


def test_tailwind_plugin_install_success(settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized and installed
    WHEN the plugin_install command is run with a valid plugin name
    THEN the plugin should be installed via npm and added to styles.css
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--tailwind-version", "4", "--no-input"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    call_command("tailwind", "install")

    # Install a plugin
    call_command("tailwind", "plugin_install", "@tailwindcss/typography")

    # Check that plugin was added to package.json
    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    with open(package_json_path) as f:
        package_json = json.load(f)
    assert "@tailwindcss/typography" in package_json["devDependencies"], (
        "Plugin should be in devDependencies"
    )

    # Check that plugin was added to styles.css
    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    with open(styles_css_path) as f:
        styles_content = f.read()
    assert '@plugin "@tailwindcss/typography";' in styles_content, (
        "Plugin directive should be in styles.css"
    )
    assert '@import "tailwindcss";' in styles_content, "Import directive should still be present"

    # Check that plugin directive is after the import
    import_index = styles_content.find('@import "tailwindcss";')
    plugin_index = styles_content.find('@plugin "@tailwindcss/typography";')
    assert import_index < plugin_index, "Plugin directive should come after import directive"


def test_tailwind_plugin_install_duplicate_prevention(settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized with a plugin already installed
    WHEN the plugin_install command is run with the same plugin name
    THEN the command should detect the duplicate and not add it again
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--tailwind-version", "4", "--no-input"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    call_command("tailwind", "install")

    # Install plugin first time
    call_command("tailwind", "plugin_install", "@tailwindcss/typography")

    # Try to install same plugin again
    call_command("tailwind", "plugin_install", "@tailwindcss/typography")

    # Check that plugin appears only once in styles.css
    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    with open(styles_css_path) as f:
        styles_content = f.read()

    plugin_count = styles_content.count('@plugin "@tailwindcss/typography";')
    assert plugin_count == 1, "Plugin directive should appear only once"


def test_tailwind_plugin_install_multiple_plugins(settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized
    WHEN multiple plugins are installed via plugin_install command
    THEN all plugins should be properly added to package.json and styles.css
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--tailwind-version", "4", "--no-input"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    call_command("tailwind", "install")

    # Install multiple plugins
    call_command("tailwind", "plugin_install", "@tailwindcss/forms")
    call_command("tailwind", "plugin_install", "@tailwindcss/typography")

    # Check package.json has both plugins
    package_json_path = os.path.join(get_app_path(app_name), "static_src", "package.json")
    with open(package_json_path) as f:
        package_json = json.load(f)
    assert "@tailwindcss/forms" in package_json["devDependencies"], (
        "First plugin should be in devDependencies"
    )
    assert "@tailwindcss/typography" in package_json["devDependencies"], (
        "Second plugin should be in devDependencies"
    )

    # Check styles.css has both plugins
    styles_css_path = os.path.join(get_app_path(app_name), "static_src", "src", "styles.css")
    with open(styles_css_path) as f:
        styles_content = f.read()
    assert '@plugin "@tailwindcss/forms";' in styles_content, (
        "First plugin directive should be in styles.css"
    )
    assert '@plugin "@tailwindcss/typography";' in styles_content, (
        "Second plugin directive should be in styles.css"
    )


def test_tailwind_plugin_install_no_plugin_name_error(settings, app_name):
    """
    GIVEN a new Tailwind v4 app is initialized
    WHEN the plugin_install command is run without a plugin name
    THEN it should raise a CommandError
    """
    call_command(
        "tailwind", "init", "--app-name", app_name, "--tailwind-version", "4", "--no-input"
    )

    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    call_command("tailwind", "install")

    # Try to install without plugin name
    with pytest.raises(Exception) as exc_info:
        call_command("tailwind", "plugin_install")

    assert "the following arguments are required: plugin_name" in str(exc_info.value)
