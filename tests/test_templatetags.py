from django.template import Context, Template


def test_tailwind_css_in_production():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({"debug": False}))

    assert '<link rel="stylesheet" href="/static/css/styles.css">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" not in output


def test_tailwind_css_in_production_with_version():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({"debug": False}))

    assert '<link rel="stylesheet" href="/static/css/styles.css?v=123">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" not in output


def test_tailwind_css_in_debug():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css %}
        """
    ).render(Context({"debug": True}))

    assert '<link rel="stylesheet" href="/static/css/styles.css">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" in output


def test_tailwind_css_in_debug_with_version():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_css v=123 %}
        """
    ).render(Context({"debug": True}))

    assert '<link rel="stylesheet" href="/static/css/styles.css?v=123">' in output
    assert "//HOST:8383/browser-sync/browser-sync-client.js" in output


def test_tailwind_preload_css():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css %}
        """
    ).render(Context())

    assert '<link rel="preload" href="/static/css/styles.css" as="style">' in output


def test_tailwind_preload_css_with_version():
    output = Template(
        """
        {% load tailwind_tags %}
        {% tailwind_preload_css v=123 %}
        """
    ).render(Context({}))

    assert (
        '<link rel="preload" href="/static/css/styles.css?v=123" as="style">' in output
    )
