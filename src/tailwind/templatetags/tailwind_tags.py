import time

from django import template
from django.conf import settings

from tailwind import get_config

from ..utils import is_path_absolute

register = template.Library()


@register.inclusion_tag("tailwind/tags/css.html")
def tailwind_css(v=None):
    if v is None and settings.DEBUG:
        # append a time-based suffix to force reload of css in dev mode
        v = int(time.time())

    return {
        "dev_mode": get_config("TAILWIND_DEV_MODE"),
        "v": v,
        "tailwind_css_path": get_config("TAILWIND_CSS_PATH"),
        "is_static_path": not is_path_absolute(get_config("TAILWIND_CSS_PATH")),
    }


@register.inclusion_tag("tailwind/tags/preload_css.html")
def tailwind_preload_css(v=None):
    return {
        "v": v,
        "tailwind_css_path": get_config("TAILWIND_CSS_PATH"),
        "is_static_path": not is_path_absolute(get_config("TAILWIND_CSS_PATH")),
    }
