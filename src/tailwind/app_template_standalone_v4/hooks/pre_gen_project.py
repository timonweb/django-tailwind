import re
import sys

APP_NAME_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

app_name = "{{ cookiecutter.app_name }}"

if not re.match(APP_NAME_REGEX, app_name):
    print(f"ERROR: {app_name} is not a valid Django app name!")

    # exits with status 1 to indicate failure
    sys.exit(1)
