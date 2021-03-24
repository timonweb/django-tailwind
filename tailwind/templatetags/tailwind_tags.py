from django import forms, template
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def tw_form(
    form, field__class: str = "", label__class: str = "", widget__class: str = ""
):
    """
    Render a default looking form with possibility to provide
    default css classes for field, label and widget.
    :param form - form object
    :param field__class - a default field (outer wrapper) css class
    :param label__class - a default label css class
    :param widget__class - a default widget css class

    Usage example:
    ```html
    {% tw_form form
        field_class="mb-3"
        label__class="font-bold"
        widget_class="w-full"
    %}
    ```
    """
    context = {
        "field__class": field__class,
        "label__class": label__class,
        "widget__class": widget__class,
    }

    has_management_form = getattr(form, "management_form", None)
    if has_management_form:
        template_name = "tailwind/forms/formset.html"
        context.update({"formset": form})
    else:
        template_name = "tailwind/forms/form.html"
        context.update({"form": form})

    return get_template(template_name).render(context)


@register.simple_tag
def tw_field(
    field,
    field__class: str = "",
    label__class: str = "",
    widget__class: str = "",
    **kwargs,
):
    """
    Render a field with provided attributes
    :param field - field object
    :param field__class - field (outer wrapper) css class
    :param label__class - label css class
    :param widget__class - widget css class

    Usage example:
    ```html
    {% tw_field form.first_name
        field__class="w-full"
        label__class="font-bold"
        widget__class="border-2 border-black
    %}
    {% tw_field form.description
        field__class="w-full h-64"
        label__class="font-bold"
        widget__class="border-2 border-blue-300
    %}
    ```

    To pass any other attribute to field, label or widget,
    prefix it with 'field__', 'label__', 'widget__'.
    Usage example:
        Given form.description is a textarea,
        we want to render it with a placeholder 'Write a message':
        ```html
        {% tw_field form.description widget__placeholder='Write a message' %}
        ```
    :return:
    """
    field_attrs = extract_attributes("field__", kwargs)
    if field__class:
        field_attrs.update({"class": field__class})

    label_attrs = extract_attributes("label__", kwargs)
    if label__class:
        label_attrs.update({"class": label__class})

    widget_attrs = extract_attributes("widget__", kwargs)

    widget_attrs = {**(field.field.widget.attrs or {}), **widget_attrs}

    if widget__class:
        existing_widget_class = field.field.widget.attrs.get("class")
        widget_attrs["class"] = (
            f"{existing_widget_class} {widget__class}"
            if existing_widget_class
            else widget__class
        )

    context = {
        "field": field,
        "field_attrs": field_attrs,
        "label_attrs": label_attrs,
        "widget_attrs": widget_attrs,
    }

    return get_template("tailwind/forms/field.html").render(context)


@register.filter
def add_last_empty_form(formset):
    return formset.forms + [formset.empty_form]


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def as_widget(field, attrs):
    return field.as_widget(attrs=attrs)


def extract_attributes(prefix: str, kwargs_dict):
    return {
        extract_attr_name(key): value
        for key, value in kwargs_dict.items()
        if key.startswith(prefix)
    }


def extract_attr_name(key):
    [_, attr_name] = key.split("__")
    return attr_name.replace("_", "-")
