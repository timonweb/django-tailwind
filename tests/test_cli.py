import os

from django.core.management import call_command


def test_tailwind_init_generates_theme_app(cleanup_theme_app, settings):
    call_command('tailwind', 'init', 'theme')
    assert os.path.isfile(os.path.join(settings.BASE_DIR, 'theme', 'apps.py')), 'The "theme" app has been generated'


def test_tailwind_install_and_build(with_theme_app, settings):
    call_command('tailwind', 'install')
    assert os.path.isfile(
        os.path.join(settings.BASE_DIR, 'theme', 'static_src', 'package.json')), 'Tailwind has been installed from npm'

    call_command('tailwind', 'build')
    assert os.path.isfile(
        os.path.join(settings.BASE_DIR, 'theme', 'static', 'css',
                     'styles.min.css')), 'Tailwind has built a css/styles.min.css file'
