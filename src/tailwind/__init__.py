import os

from django.conf import settings


def get_config(setting_name):
    tailwind_css_path = getattr(settings, "TAILWIND_CSS_PATH", "css/dist/styles.css")
    return {
        "NPM_BIN_PATH": getattr(settings, "NPM_BIN_PATH", "npm"),
        # 'TAILWIND_DEV_MODE' is deprecated. Leaving it here
        # to support legacy browser-sync based configs.
        "TAILWIND_DEV_MODE": getattr(settings, "TAILWIND_DEV_MODE", False),
        "TAILWIND_CSS_PATH": tailwind_css_path,
        "TAILWIND_APP_NAME": getattr(settings, "TAILWIND_APP_NAME", None),
        "TAILWIND_USE_STANDALONE_BINARY": getattr(
            settings, "TAILWIND_USE_STANDALONE_BINARY", False
        ),
        "TAILWIND_STANDALONE_BINARY_VERSION": getattr(
            settings,
            "TAILWIND_STANDALONE_BINARY_VERSION",
            os.environ.get("TAILWINDCSS_VERSION", "v4.1.16"),
        ),
        "TAILWIND_STANDALONE_START_COMMAND_ARGS": getattr(
            settings,
            "TAILWIND_STANDALONE_START_COMMAND_ARGS",
            f"-i static_src/src/styles.css -o static/{tailwind_css_path} --watch",
        ),
        "TAILWIND_STANDALONE_BUILD_COMMAND_ARGS": getattr(
            settings,
            "TAILWIND_STANDALONE_BUILD_COMMAND_ARGS",
            f"-i static_src/src/styles.css -o static/{tailwind_css_path} --minify",
        ),
    }[setting_name]
