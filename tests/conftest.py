import os
import shutil
import pytest
from django.core.management import call_command
from tailwind.utils import get_app_path


def cleanup_theme_app_dir(app_name):
    theme_app_dir = get_app_path(app_name)
    if os.path.isdir(theme_app_dir):
        shutil.rmtree(theme_app_dir)
