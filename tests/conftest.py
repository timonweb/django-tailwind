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
def app_name():
    return f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'


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
