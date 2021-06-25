from django import template

from ..conf import TAILWIND_CSS_PATH, TAILWIND_DEV_MODE
from ..utils import is_path_absolute

register = template.Library()


@register.inclusion_tag("tailwind/tags/css.html")
def tailwind_css(v=None):
    return {
        "debug": TAILWIND_DEV_MODE,
        "v": v,
        "tailwind_css_path": TAILWIND_CSS_PATH,
        "is_static_path": not is_path_absolute(TAILWIND_CSS_PATH),
    }


@register.inclusion_tag("tailwind/tags/preload_css.html")
def tailwind_preload_css(v=None):
    return {
        "v": v,
        "tailwind_css_path": TAILWIND_CSS_PATH,
        "is_static_path": not is_path_absolute(TAILWIND_CSS_PATH),
    }
