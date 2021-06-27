from django.conf import settings


def get_config(setting_name):
    return {
        "NPM_BIN_PATH": getattr(settings, "NPM_BIN_PATH", "npm"),
        "TAILWIND_DEV_MODE": getattr(settings, "TAILWIND_DEV_MODE", settings.DEBUG),
        "TAILWIND_CSS_PATH": getattr(
            settings, "TAILWIND_CSS_PATH", "css/dist/styles.css"
        ),
        "TAILWIND_APP_NAME": getattr(settings, "TAILWIND_APP_NAME"),
    }[setting_name]
