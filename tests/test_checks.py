from django.core import checks


def get_tailwind_check_ids():
    return [message.id for message in checks.run_checks() if message.id.startswith("tailwind.")]


def test_check_warns_when_tailwind_app_name_is_not_set(settings):
    """
    GIVEN the test settings, which do not define TAILWIND_APP_NAME
    WHEN Django system checks are run
    THEN the tailwind.W001 warning should be reported
    """
    assert not hasattr(settings, "TAILWIND_APP_NAME")
    assert get_tailwind_check_ids() == ["tailwind.W001"]


def test_check_warns_when_tailwind_app_name_is_empty(settings):
    """
    GIVEN TAILWIND_APP_NAME is set to an empty value
    WHEN Django system checks are run
    THEN the tailwind.W001 warning should be reported
    """
    settings.TAILWIND_APP_NAME = ""

    assert get_tailwind_check_ids() == ["tailwind.W001"]


def test_check_warns_when_tailwind_app_is_not_installed(settings):
    """
    GIVEN TAILWIND_APP_NAME points at an app that is not in INSTALLED_APPS
    WHEN Django system checks are run
    THEN the tailwind.W002 warning should be reported
    """
    settings.TAILWIND_APP_NAME = "theme"

    assert get_tailwind_check_ids() == ["tailwind.W002"]


def test_check_passes_for_installed_tailwind_app(settings):
    """
    GIVEN TAILWIND_APP_NAME points at an app listed in INSTALLED_APPS
    WHEN Django system checks are run
    THEN no tailwind warnings should be reported
    """
    settings.TAILWIND_APP_NAME = "tests"
    settings.INSTALLED_APPS += ["tests"]

    assert get_tailwind_check_ids() == []
