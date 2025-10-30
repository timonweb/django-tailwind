import contextlib
import os
import platform
import signal
import subprocess

from django.core.management.base import CommandError
from django.core.management.base import LabelCommand

from tailwind import get_config

from ...npm import NPM
from ...npm import NPMException
from ...utils import extract_server_url_from_procfile
from ...utils import get_tailwind_src_path
from ...utils import install_pip_package
from ...validate import ValidationError
from ...validate import Validations


class Command(LabelCommand):
    help = "Runs tailwind commands"
    missing_args_message = """
Command argument is missing, please add one of the following:
  init - to initialize django-tailwind app
  install - to install npm packages necessary to build tailwind css
  build - to compile tailwind css into production css
  start - to start watching css changes for dev
  dev - to start Django server and Tailwind watcher simultaneously
  check-updates - to list possible updates for tailwind css and its dependencies
  update - to update tailwind css and its dependencies
  plugin_install <plugin-name> - to install and configure a tailwind plugin
Usage example:
  python manage.py tailwind start
"""
    npm = None
    validate = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate = Validations()

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Initializes Tailwind project without user prompts",
        )
        parser.add_argument(
            "--tailwind-version",
            default="4",
            choices=["3", "4"],
            help="Specifies the Tailwind version to install",
        )
        parser.add_argument(
            "--app-name",
            help="Sets default app name on Tailwind project initialization",
        )
        parser.add_argument(
            "--no-package-lock",
            action="store_true",
            help="Disables package-lock.json creation during install",
        )
        parser.add_argument(
            "--include-daisy-ui",
            action="store_true",
            help="Includes DaisyUI component library in the Tailwind project",
        )

    def validate_app(self):
        try:
            self.validate.has_settings()
            app_name = get_config("TAILWIND_APP_NAME")
            self.validate.is_installed(app_name)
            self.validate.is_tailwind_app(app_name)
        except ValidationError as err:
            raise CommandError(err) from err

    def handle(self, *labels, **options):
        return self.handle_labels(*labels, **options)

    def handle_labels(self, *labels, **options):
        self.validate.acceptable_label(labels[0])
        if labels[0] != "init":
            self.validate_app()
            self.npm = NPM(cwd=get_tailwind_src_path(get_config("TAILWIND_APP_NAME")))

        getattr(self, "handle_" + labels[0].replace("-", "_") + "_command")(*labels[1:], **options)

    def handle_init_command(self, **options):
        try:
            from cookiecutter.main import cookiecutter
        except ImportError:
            self.stdout.write("Cookiecutter is not found, installing...")
            try:
                install_pip_package("cookiecutter")
                from cookiecutter.main import cookiecutter
            except ModuleNotFoundError as err:
                raise CommandError(
                    "Failed to install 'cookiecutter' via pip. Please install it manually "
                    "(https://pypi.org/project/cookiecutter/) and run 'python manage.py tailwind init' again."
                ) from err

        try:
            app_path = cookiecutter(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                output_dir=os.getcwd(),
                directory=f"app_template_v{options['tailwind_version']}",
                no_input=options["no_input"],
                overwrite_if_exists=False,
                extra_context={
                    "app_name": options["app_name"].strip() if options.get("app_name") else "theme",
                    "include_daisy_ui": "yes" if options.get("include_daisy_ui") else "no",
                },
            )

            app_name = os.path.basename(app_path)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Tailwind application '{app_name}' "
                    f"has been successfully created. "
                    f"Please add '{app_name}' to INSTALLED_APPS in settings.py, "
                    f"and declare TAILWIND_APP_NAME = '{app_name}' in settings.py, "
                    f"then run the following command to install Tailwind CSS "
                    f"dependencies: `python manage.py tailwind install`"
                )
            )
        except Exception as err:
            raise CommandError(err) from err

    def handle_install_command(self, **options):
        args = ["install"]
        if options["no_package_lock"]:
            args.append("--no-package-lock")

        self.npm_command(*args)

        # Run the build command after installation
        self.npm_command("run", "build")

    def handle_build_command(self, **options):
        self.npm_command("run", "build")

    def handle_start_command(self, **options):
        self.npm_command("run", "start")

    def handle_dev_command(self, **options):
        # Check if honcho is installed
        try:
            subprocess.run(["honcho", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.stdout.write("Honcho is not installed. Installing honcho...")
            try:
                install_pip_package("honcho")
                self.stdout.write(self.style.SUCCESS("Honcho installed successfully!"))
            except Exception as err:
                raise CommandError(
                    "Failed to install 'honcho' via pip. Please install it manually "
                    "(https://pypi.org/project/honcho/) and run 'python manage.py tailwind dev' again."
                ) from err

        # Check if Procfile.tailwind exists, create if not
        procfile_path = os.path.join(os.getcwd(), "Procfile.tailwind")
        if not os.path.exists(procfile_path):
            self.stdout.write("Creating Procfile.tailwind...")
            procfile_content = """django: python manage.py runserver
tailwind: python manage.py tailwind start"""
            with open(procfile_path, "w") as f:
                f.write(procfile_content)
            self.stdout.write(
                self.style.SUCCESS(
                    "Procfile.tailwind created! You can customize the Django runserver command in this file."
                )
            )

        # Print a message with the server URL
        message = "🚀 Starting Tailwind watcher and Django development server"
        line = "#" * (len(message) + 1)

        self.stdout.write(line)
        self.stdout.write(message)
        if server_url := extract_server_url_from_procfile(procfile_path):
            self.stdout.write(self.style.SUCCESS(f"   You can access the server at: {server_url}"))
        self.stdout.write("   Press Ctrl+C to stop the servers")
        self.stdout.write(line)
        self.stdout.write("")

        # Start honcho with the Procfile
        try:
            self.run_honcho("Procfile.tailwind")
        except subprocess.CalledProcessError as err:
            raise CommandError(f"Failed to start honcho: {err}") from err
        except KeyboardInterrupt:
            self.stdout.write("\nStopping development servers...")

    def run_honcho(self, procfile, extra_args=None) -> int:
        """
        Runs Honcho in a way that Ctrl+C works:
          - Windows: wraps with `cmd /c` and uses a new process group
          - POSIX (Linux/macOS/WSL): runs directly
        Returns the exit code.
        """
        extra_args = list(extra_args or [])
        base_cmd = ["honcho", "-f", procfile, "start", *extra_args]

        # Let Ctrl+C (SIGINT) interrupt the subprocess too
        # On some embedded environments this may not be available; ignore.
        with contextlib.suppress(Exception):
            signal.signal(signal.SIGINT, signal.SIG_DFL)

        system = platform.system()
        is_windows = system == "Windows"

        if is_windows:
            # On native Windows, wrap with `cmd /c` so Ctrl+C propagates reliably
            cmd = ["cmd", "/c", *base_cmd]
            creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            return subprocess.run(
                cmd,
                check=False,
                creationflags=creationflags,
            ).returncode
        else:
            # Linux/macOS/WSL: plain run
            return subprocess.run(base_cmd, check=False).returncode

    def handle_check_updates_command(self, **options):
        self.npm_command("outdated")

    def handle_update_command(self, **options):
        self.npm_command("update")

    def handle_plugin_install_command(self, *labels, **options):
        if not labels:
            raise CommandError(
                "Plugin name is required. Usage: python manage.py tailwind plugin_install <plugin-name>"
            )

        plugin_name = labels[0]

        # Install the npm package
        self.stdout.write(f"Installing {plugin_name} npm package...")
        try:
            self.npm_command("install", plugin_name, "--save-dev")
            self.stdout.write(
                self.style.SUCCESS(f"Successfully installed {plugin_name} npm package")
            )
        except Exception as err:
            raise CommandError(f"Failed to install {plugin_name}: {err}") from err

        # Update styles.css to include the plugin
        app_name = get_config("TAILWIND_APP_NAME")
        styles_path = os.path.join(get_tailwind_src_path(app_name), "src", "styles.css")

        if not os.path.exists(styles_path):
            raise CommandError(f"styles.css not found at {styles_path}")

        # Read current styles.css content
        with open(styles_path) as f:
            content = f.read()

        # Check if plugin is already included
        plugin_line = f'@plugin "{plugin_name}";'
        if plugin_line in content:
            self.stdout.write(
                self.style.WARNING(f"Plugin {plugin_name} is already included in styles.css")
            )
            return

        # Add plugin line after @import "tailwindcss"
        import_line = '@import "tailwindcss";'
        if import_line not in content:
            raise CommandError('Could not find @import "tailwindcss"; in styles.css')

        # Insert plugin line after the import
        new_content = content.replace(import_line, f'{import_line}\n@plugin "{plugin_name}";\n')

        # Write updated content back to file
        with open(styles_path, "w") as f:
            f.write(new_content)

        self.stdout.write(self.style.SUCCESS(f"Successfully added {plugin_name} to styles.css"))
        self.stdout.write(f"Plugin {plugin_name} has been installed and configured!")

    def npm_command(self, *args):
        try:
            self.npm.command(*args)
        except NPMException as err:
            raise CommandError(err) from err
        except KeyboardInterrupt:
            pass
