import json
import os
import re

from django.apps import apps

DJANGO_TAILWIND_APP_DIR = os.path.dirname(__file__)


def get_app_path(app_name):
    app_label = app_name.split(".")[-1]
    return apps.get_app_config(app_label).path


def get_tailwind_src_path(app_name):
    return os.path.join(get_app_path(app_name), "static_src")


def get_package_json_path(app_name):
    return os.path.join(get_app_path(app_name), "static_src", "package.json")


def get_package_json_contents(app_name):
    with open(get_package_json_path(app_name)) as f:
        return json.load(f)


def is_path_absolute(path):
    return path.startswith(("/", "http"))


def install_pip_package(package):
    import pip._internal as pip

    pip.main(["install", package])


def extract_server_url_from_procfile(procfile_path):
    """Extract the Django development server URL from Procfile.tailwind"""
    try:
        with open(procfile_path) as f:
            content = f.read()

        # Look for the django process line
        for line in content.strip().split("\n"):
            if line.strip().startswith("django:"):
                command = line.split(":", 1)[1].strip()
                protocol = extract_protocol_from_command(command)
                host, port = extract_host_and_port(command)
                return f"{protocol}://{host}:{port}/"
        return None

    except Exception:
        return None


def extract_protocol_from_command(command):
    protocol = "http"
    if any(
        [
            "--ssl" in command,
            "--secure" in command,
            "--https" in command,
            "--cert" in command,
        ]
    ):
        protocol = "https"
    return protocol


def extract_host_and_port(command):
    host = "127.0.0.1"
    port = "8000"

    # Extract IP address/hostname pattern (IPv4, IPv6, or hostname)
    # Matches patterns like: 127.0.0.1, 0.0.0.0, localhost, example.com, ::1, [::1]
    host_match = re.search(
        r"(?:^|\s)(?:\[?([a-fA-F0-9]*:[a-fA-F0-9:]*)\]?|([0-9]{1,3}(?:\.[0-9]{1,3}){3})|(localhost))(?::|$|\s)",
        command,
    )
    if host_match:
        # Get the first non-None group (IPv6, IPv4, or hostname)
        matched_host = host_match.group(1) or host_match.group(2) or host_match.group(3)
        if matched_host:
            host = matched_host

    # Extract port pattern (digits after colon OR standalone digits)
    # Matches either ":PORT" or " PORT" format
    port_match = re.search(r":(\d+)(?:\s|$)|\s(\d+)(?:\s|$)", command)
    if port_match:
        port = port_match.group(1) or port_match.group(2)

    return host, port
