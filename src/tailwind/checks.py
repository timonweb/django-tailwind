from django.core.checks import register
from django.core.checks import Warning

from tailwind import get_config

from .validate import ValidationError
from .validate import Validations


@register()
def check_tailwind_app(app_configs, **kwargs):
    validate = Validations()

    try:
        validate.has_settings()
    except ValidationError as err:
        return [
            Warning(
                str(err),
                hint=(
                    "Create a Tailwind app with 'python manage.py tailwind init' and set "
                    "TAILWIND_APP_NAME to its name."
                ),
                id="tailwind.W001",
            )
        ]

    try:
        validate.is_installed(get_config("TAILWIND_APP_NAME"))
    except ValidationError as err:
        return [
            Warning(
                str(err),
                hint="Add the Tailwind app named in TAILWIND_APP_NAME to INSTALLED_APPS.",
                id="tailwind.W002",
            )
        ]

    return []
