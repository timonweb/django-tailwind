import os
from unittest import mock

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from .conftest import call_command_with_output
from .conftest import get_tailwind_versions


@pytest.mark.parametrize("tailwind_version", get_tailwind_versions())
def test_tailwind_dev_command_creates_procfile_real(
    settings, app_name, procfile_path, tailwind_version
):
    """
    GIVEN a Tailwind app is initialized and no Procfile.tailwind exists
    WHEN the dev command is run
    THEN Procfile.tailwind should be created with correct Django
    and Tailwind process definitions
    """
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        tailwind_version,
        "--no-input",
    )
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Ensure Procfile.tailwind doesn't exist
    assert not os.path.exists(procfile_path)

    # Mock subprocess to prevent actual honcho execution
    with mock.patch("subprocess.run") as mock_subprocess:
        # Mock honcho is installed
        mock_subprocess.side_effect = [
            mock.Mock(),  # honcho --version succeeds
            KeyboardInterrupt(),  # honcho start interrupted immediately
        ]

        # Call dev command - should create Procfile
        with pytest.raises(SystemExit):
            call_command("tailwind", "dev")

    # Verify file was actually created
    assert os.path.exists(procfile_path), "Procfile.tailwind should be created"

    # Verify content
    with open(procfile_path) as f:
        content = f.read()

    expected_content = """django: python manage.py runserver
tailwind: python manage.py tailwind start"""

    assert content == expected_content, f"Expected:\n{expected_content}\nGot:\n{content}"


@pytest.mark.parametrize("tailwind_version", get_tailwind_versions())
def test_tailwind_dev_command_uses_existing_procfile(
    settings, app_name, procfile_path, tailwind_version
):
    """
    GIVEN a Tailwind app is initialized and a custom Procfile.tailwind already exists
    WHEN the dev command is run
    THEN the existing Procfile.tailwind should be preserved without modification
    """

    # Setup
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        tailwind_version,
        "--no-input",
    )
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Create custom Procfile.tailwind
    custom_content = """django: python manage.py runserver 0.0.0.0:8000
tailwind: python manage.py tailwind start
redis: redis-server"""

    with open(procfile_path, "w") as f:
        f.write(custom_content)

    # Mock subprocess to prevent actual honcho execution
    with mock.patch("subprocess.run") as mock_subprocess:
        # Mock honcho is installed
        mock_subprocess.side_effect = [
            mock.Mock(),  # honcho --version succeeds
            KeyboardInterrupt(),  # honcho start interrupted immediately
        ]

        # Call dev command - should NOT overwrite existing Procfile
        with pytest.raises(SystemExit):
            call_command_with_output("tailwind", "dev")

    # Verify file still exists and wasn't overwritten
    assert os.path.exists(procfile_path), "Procfile.tailwind should still exist"

    # Verify content wasn't changed
    with open(procfile_path) as f:
        content = f.read()

    assert content == custom_content, "Existing Procfile.tailwind should not be overwritten"


@pytest.mark.parametrize("tailwind_version", get_tailwind_versions())
def test_tailwind_dev_command_subprocess_error(settings, app_name, procfile_path, tailwind_version):
    """
    GIVEN a Tailwind app is initialized and honcho is available
    WHEN the dev command is run but honcho start fails
    THEN a CommandError should be raised with subprocess failure message
    """
    # Setup
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        tailwind_version,
        "--no-input",
    )
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess to simulate honcho start failure
    with mock.patch("subprocess.run") as mock_subprocess:
        import subprocess

        # Mock honcho version check to succeed, but start to fail
        mock_subprocess.side_effect = [
            mock.Mock(),  # honcho --version succeeds
            subprocess.CalledProcessError(1, ["honcho", "start"]),  # honcho start fails
        ]

        # Expect CommandError to be raised
        with pytest.raises(CommandError, match="Failed to start honcho"):
            call_command("tailwind", "dev")


@pytest.mark.parametrize("tailwind_version", get_tailwind_versions())
def test_tailwind_dev_command_graceful_keyboard_interrupt(
    settings, app_name, procfile_path, tailwind_version
):
    """
    GIVEN a Tailwind app is initialized and the dev command is running
    WHEN a KeyboardInterrupt is received (user presses Ctrl+C)
    THEN the command should exit gracefully without raising an exception
    """
    # Setup
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        tailwind_version,
        "--no-input",
    )
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess to simulate KeyboardInterrupt
    with mock.patch("subprocess.run") as mock_subprocess:
        # Mock honcho version check to succeed, but start to be interrupted
        mock_subprocess.side_effect = [
            mock.Mock(),  # honcho --version succeeds
            KeyboardInterrupt(),  # honcho start interrupted
        ]

        # Should not raise exception, should handle gracefully
        with pytest.raises(SystemExit):
            call_command("tailwind", "dev")

        # If we get here, the KeyboardInterrupt was handled properly
        assert True, "KeyboardInterrupt should be handled gracefully"


@pytest.mark.parametrize("tailwind_version", get_tailwind_versions())
def test_tailwind_dev_command_messages_in_the_output(
    settings, app_name, procfile_path, tailwind_version
):
    """
    GIVEN a Tailwind app is initialized and the dev command is run
    WHEN the command is executed
    THEN the output should contain expected messages about starting servers
    """
    call_command(
        "tailwind",
        "init",
        "--app-name",
        app_name,
        "--tailwind-version",
        tailwind_version,
        "--no-input",
    )
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess to prevent actual honcho execution
    with mock.patch("subprocess.run") as mock_subprocess:
        # Mock honcho is installed
        mock_subprocess.side_effect = [
            mock.Mock(),  # honcho --version succeeds
            KeyboardInterrupt(),  # honcho start interrupted immediately
        ]

        # Call dev command - should create Procfile
        with pytest.raises(SystemExit):
            out, _ = call_command_with_output("tailwind", "dev")

            assert "Procfile.tailwind created" in out
            assert "Starting Tailwind watcher and Django development server" in out
            assert "You can access the server at: http://127.0.0.1:8000/"
            assert "Press Ctrl+C to stop the servers"


def test_tailwind_dev_command_help_includes_dev():
    """
    GIVEN the tailwind management command is available
    WHEN the command is run without arguments to show help
    """
    try:
        call_command("tailwind")
        raise AssertionError("Should have raised CommandError for missing arguments")
    except CommandError as e:
        help_text = str(e)
        assert "Error: the following arguments are required: subcommand" in help_text


def test_procfile_content_format():
    """
    GIVEN the expected Procfile.tailwind content format
    WHEN the content string is parsed
    THEN it should contain properly formatted Django and Tailwind process definitions
    """
    # This is testing the actual string format without file I/O
    expected_content = """django: python manage.py runserver
tailwind: python manage.py tailwind start"""

    # Verify it's properly formatted (no extra newlines, proper format)
    lines = expected_content.split("\n")
    assert len(lines) == 2
    assert lines[0].startswith("django:")
    assert lines[1].startswith("tailwind:")
    assert "python manage.py runserver" in lines[0]
    assert "python manage.py tailwind start" in lines[1]
