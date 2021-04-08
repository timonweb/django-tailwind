from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("tailwind/tags/css.html", takes_context=True)
def tailwind_css(context, v=None):
    return {
        "debug": context.get("debug", False),
        "v": v,
        "tailwind_app_name": settings.TAILWIND_APP_NAME,
    }


@register.inclusion_tag("tailwind/tags/preload_css.html")
def tailwind_preload_css(v=None):
    return {"v": v, "tailwind_app_name": settings.TAILWIND_APP_NAME}
