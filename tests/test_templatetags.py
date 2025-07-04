import time

from django.template import Context, Template


def test_tailwind_css_in_production(settings):
    """
    GIVEN Tailwind is configured for production mode (DEBUG=False)
    WHEN the tailwind_css template tag is rendered
    THEN it should output a link tag with the static CSS path without cache-busting
    """
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" type="text/css" href="/static/css/dist/styles.css">' in output


def test_tailwind_css_in_production_with_version(settings):
    """
    GIVEN Tailwind is configured for production mode with a specific version parameter
    WHEN the tailwind_css template tag is rendered with v=123
    THEN it should output a link tag with the static CSS path including the version parameter
    """
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" type="text/css" href="/static/css/dist/styles.css?v=123">' in output


def test_tailwind_css_in_debug(settings):
    """
    GIVEN Tailwind is configured for debug mode (DEBUG=True)
    WHEN the tailwind_css template tag is rendered without version
    THEN it should output a link tag with automatic timestamp-based cache-busting
    """
    settings.TAILWIND_APP_NAME = "theme"
    settings.DEBUG = True
    partial_time_version = str(int(time.time()))[:7]

    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({}))

    assert (
        f'<link rel="stylesheet" type="text/css" href="/static/css/dist/styles.css?v={partial_time_version}' in output
    )


def test_tailwind_css_in_legacy_tailwind_dev_mode(settings):
    """
    GIVEN Tailwind is configured with legacy TAILWIND_DEV_MODE=True
    WHEN the tailwind_css template tag is rendered
    THEN it should output a link tag with the static CSS path without cache-busting
    """
    settings.TAILWIND_APP_NAME = "theme"
    settings.TAILWIND_DEV_MODE = True

    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" type="text/css" href="/static/css/dist/styles.css">' in output


def test_tailwind_css_in_debug_with_version(settings):
    """
    GIVEN Tailwind is configured and a specific version is provided
    WHEN the tailwind_css template tag is rendered with v=123
    THEN it should output a link tag with the specified version parameter overriding debug mode
    """
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" type="text/css" href="/static/css/dist/styles.css?v=123">' in output


def test_tailwind_preload_css(settings):
    """
    GIVEN Tailwind is configured
    WHEN the tailwind_preload_css template tag is rendered
    THEN it should output a preload link tag for CSS optimization
    """
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css %}
        """
    ).render(Context())

    assert '<link rel="preload" href="/static/css/dist/styles.css" as="style">' in output


def test_tailwind_preload_css_with_version(settings):
    """
    GIVEN Tailwind is configured with a specific version parameter
    WHEN the tailwind_preload_css template tag is rendered with v=123
    THEN it should output a preload link tag with the version parameter
    """
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css v=123 %}
        """
    ).render(Context())

    assert '<link rel="preload" href="/static/css/dist/styles.css?v=123" as="style">' in output
