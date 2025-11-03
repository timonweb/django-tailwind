import os
from unittest import mock

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from .conftest import call_command_with_output


def test_tailwind_dev_command_creates_procfile_real(settings, app_name, procfile_path):
    """
    GIVEN a Tailwind app is initialized and no Procfile.tailwind exists
    WHEN the dev command is run
    THEN Procfile.tailwind should be created with correct Django
    and Tailwind process definitions
    """
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Ensure Procfile.tailwind doesn't exist
    assert not os.path.exists(procfile_path)

    # Mock subprocess.Popen to prevent actual process execution
    with mock.patch("subprocess.Popen") as mock_popen, mock.patch("time.sleep") as mock_sleep:
        mock_proc = mock.Mock()
        mock_proc.poll.return_value = None  # Process is running
        mock_proc.wait.return_value = None
        mock_proc.terminate.return_value = None
        mock_popen.return_value = mock_proc

        # Simulate KeyboardInterrupt after first sleep
        mock_sleep.side_effect = KeyboardInterrupt()

        # Call dev command - should create Procfile
        call_command("tailwind", "dev")

    # Verify file was actually created
    assert os.path.exists(procfile_path), "Procfile.tailwind should be created"

    # Verify content
    with open(procfile_path) as f:
        content = f.read()

    expected_content = """django: python manage.py runserver
tailwind: python manage.py tailwind start"""

    assert content == expected_content, f"Expected:\n{expected_content}\nGot:\n{content}"


def test_tailwind_dev_command_uses_existing_procfile(settings, app_name, procfile_path):
    """
    GIVEN a Tailwind app is initialized and a custom Procfile.tailwind already exists
    WHEN the dev command is run
    THEN the existing Procfile.tailwind should be preserved without modification
    """

    # Setup
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Create custom Procfile.tailwind
    custom_content = """django: python manage.py runserver 0.0.0.0:8000
tailwind: python manage.py tailwind start
redis: redis-server"""

    with open(procfile_path, "w") as f:
        f.write(custom_content)

    # Mock subprocess.Popen to prevent actual process execution
    with mock.patch("subprocess.Popen") as mock_popen, mock.patch("time.sleep") as mock_sleep:
        mock_proc = mock.Mock()
        mock_proc.poll.return_value = None
        mock_proc.wait.return_value = None
        mock_proc.terminate.return_value = None
        mock_popen.return_value = mock_proc
        mock_sleep.side_effect = KeyboardInterrupt()

        # Call dev command - should NOT overwrite existing Procfile
        call_command_with_output("tailwind", "dev")

    # Verify file still exists and wasn't overwritten
    assert os.path.exists(procfile_path), "Procfile.tailwind should still exist"

    # Verify content wasn't changed
    with open(procfile_path) as f:
        content = f.read()

    assert content == custom_content, "Existing Procfile.tailwind should not be overwritten"


def test_tailwind_dev_command_subprocess_error(settings, app_name, procfile_path):
    """
    GIVEN a Tailwind app is initialized
    WHEN the dev command is run but a process exits unexpectedly
    THEN a CommandError should be raised
    """
    # Setup
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess.Popen to simulate process failure
    with mock.patch("subprocess.Popen") as mock_popen:
        mock_proc = mock.Mock()
        mock_proc.poll.return_value = 1  # Process exited with error code 1
        mock_proc.returncode = 1
        mock_popen.return_value = mock_proc

        # Expect CommandError to be raised
        with pytest.raises(CommandError, match="A process exited unexpectedly"):
            call_command("tailwind", "dev")


def test_tailwind_dev_command_graceful_keyboard_interrupt(settings, app_name, procfile_path):
    """
    GIVEN a Tailwind app is initialized and the dev command is running
    WHEN a KeyboardInterrupt is received (user presses Ctrl+C)
    THEN the command should exit gracefully without raising an exception
    """
    # Setup
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess.Popen to simulate KeyboardInterrupt
    with mock.patch("subprocess.Popen") as mock_popen, mock.patch("time.sleep") as mock_sleep:
        mock_proc = mock.Mock()
        mock_proc.poll.return_value = None
        mock_proc.wait.return_value = None
        mock_proc.terminate.return_value = None
        mock_popen.return_value = mock_proc
        mock_sleep.side_effect = KeyboardInterrupt()

        # Should not raise exception, should handle gracefully
        call_command("tailwind", "dev")

        # If we get here, the KeyboardInterrupt was handled properly
        assert True, "KeyboardInterrupt should be handled gracefully"


def test_tailwind_dev_command_messages_in_the_output(settings, app_name, procfile_path):
    """
    GIVEN a Tailwind app is initialized and the dev command is run
    WHEN the command is executed
    THEN the output should contain expected messages about starting servers
    """
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    # Mock subprocess.Popen to prevent actual process execution
    with mock.patch("subprocess.Popen") as mock_popen, mock.patch("time.sleep") as mock_sleep:
        mock_proc = mock.Mock()
        mock_proc.poll.return_value = None
        mock_proc.wait.return_value = None
        mock_proc.terminate.return_value = None
        mock_popen.return_value = mock_proc
        mock_sleep.side_effect = KeyboardInterrupt()

        # Call dev command - should create Procfile
        out, _ = call_command_with_output("tailwind", "dev")

        assert "Procfile.tailwind created" in out
        assert "Starting Tailwind watcher and Django development server" in out
        assert "You can access the server at: http://127.0.0.1:8000/"
        assert "Press Ctrl+C to stop the servers"


def test_tailwind_dev_command_help_includes_dev():
    """
    GIVEN the tailwind management command is available
    WHEN the command is run without arguments to show help
    THEN the help text should include the dev command description
    """
    # This tests the actual help message without mocking
    try:
        call_command("tailwind")
        raise AssertionError("Should have raised CommandError for missing arguments")
    except CommandError as e:
        help_text = str(e)
        assert "dev - to start Django server and Tailwind watcher simultaneously" in help_text
        assert "python manage.py tailwind start" in help_text  # Usage example should be there


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
