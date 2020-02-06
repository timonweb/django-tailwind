import os
import shutil

import pytest
from django.core.management import call_command


@pytest.yield_fixture
def cleanup_theme_app(settings):
    theme_app_dir = os.path.join(settings.BASE_DIR, 'theme')
    if os.path.isdir(theme_app_dir):
        shutil.rmtree(theme_app_dir)
    yield
    if os.path.isdir(theme_app_dir):
        shutil.rmtree(theme_app_dir)


@pytest.fixture()
def with_theme_app(cleanup_theme_app, settings):
    call_command('tailwind', 'init', 'theme')
    settings.INSTALLED_APPS += ['theme']
    settings.TAILWIND_APP_NAME = 'theme'
    yield
