from django.conf import settings

NPM_BIN_PATH = getattr(settings, "NPM_BIN_PATH", "npm")
TAILWIND_CSS_PATH = getattr(settings, "TAILWIND_CSS_PATH", "css/dist/styles.css")
TAILWIND_DEV_MODE = getattr(settings, "TAILWIND_DEV_MODE", settings.DEBUG)
