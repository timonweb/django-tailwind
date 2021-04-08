from django import template

register = template.Library()


@register.inclusion_tag("tailwind/tags/css.html", takes_context=True)
def tailwind_css(context):
    return {"debug": context.get("debug", False)}
