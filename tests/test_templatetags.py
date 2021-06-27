from django.template import Context, Template


def test_tailwind_css_in_production(settings):
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" href="/static/css/dist/styles.css">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" not in output


def test_tailwind_css_in_production_with_version(settings):
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" href="/static/css/dist/styles.css?v=123">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" not in output


def test_tailwind_css_in_debug(settings):
    settings.TAILWIND_APP_NAME = "theme"
    settings.TAILWIND_DEV_MODE = True
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" href="/static/css/dist/styles.css">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" in output


def test_tailwind_css_in_debug_with_version(settings):
    settings.TAILWIND_APP_NAME = "theme"
    settings.TAILWIND_DEV_MODE = True
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({}))

    assert '<link rel="stylesheet" href="/static/css/dist/styles.css?v=123">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" in output


def test_tailwind_preload_css(settings):
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css %}
        """
    ).render(Context())

    assert (
        '<link rel="preload" href="/static/css/dist/styles.css" as="style">' in output
    )


def test_tailwind_preload_css_with_version(settings):
    settings.TAILWIND_APP_NAME = "theme"
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css v=123 %}
        """
    ).render(Context())

    assert (
        '<link rel="preload" href="/static/css/dist/styles.css?v=123" as="style">'
        in output
    )
