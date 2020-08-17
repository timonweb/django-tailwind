import os
from django.core.management import call_command
from tailwind.utils import get_app_path
from .conftest import cleanup_theme_app_dir


def test_tailwind_install_and_build(settings):
    call_command('tailwind', 'init', 'theme')
    settings.INSTALLED_APPS += ['theme']
    settings.TAILWIND_APP_NAME = 'theme'

    assert os.path.isfile(
        os.path.join(get_app_path("theme"), "apps.py")
    ), 'The "theme" app has been generated'

    call_command("tailwind", "install")
    assert os.path.isfile(
        os.path.join(get_app_path("theme"), "static_src", "package.json")
    ), "Tailwind has been installed from npm"

    call_command("tailwind", "build")
    assert os.path.isfile(
        os.path.join(get_app_path("theme"), "static", "css", "styles.css")
    ), "Tailwind has built a css/styles.css file"

    cleanup_theme_app_dir('theme')
