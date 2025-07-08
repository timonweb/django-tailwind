import os
import shutil
import uuid
from io import StringIO

import pytest
from django.conf import settings
from django.core.management import call_command as django_call_command


def cleanup_theme_app_dir(app_name):
    app_dir = os.path.join(settings.BASE_DIR, app_name)
    if os.path.isdir(app_dir):
        shutil.rmtree(app_dir)


@pytest.fixture
def app_name3():
    return f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'


@pytest.fixture
def app_name():
    name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'
    yield name
    print(f"Cleaning up app {name}")
    cleanup_theme_app_dir(name)


@pytest.fixture
def procfile_path():
    """
    Fixture to clean up the Procfile.tailwind after each test.
    """
    procfile_path = os.path.join(settings.BASE_DIR, "Procfile.tailwind")
    yield procfile_path
    if os.path.exists(procfile_path):
        os.remove(procfile_path)


def call_command_with_output(command_name, *args, **kwargs):
    out = StringIO()
    err = StringIO()
    django_call_command(
        command_name,
        *args,
        stdout=out,
        stderr=err,
        **kwargs,
    )
    return out.getvalue(), err.getvalue()
