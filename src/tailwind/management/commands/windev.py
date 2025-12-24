"""
Run the Django dev server and Tailwind watcher synced in WT.

command reference: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd
"""

import subprocess

project_dir = r"project dir here"

subprocess.run([
    "wt",
    "new-tab", "cmd", "/k", f"cd /d {project_dir} && python manage.py runserver",
    ";",
    "split-pane", "/k", f"cd /d {project_dir} && python manage.py tailwind start"
])
