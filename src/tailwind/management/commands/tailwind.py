import os
import platform
import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from tailwind import get_config

from ...npm import NPM
from ...npm import NPMException
from ...utils import extract_server_url_from_procfile
from ...utils import get_app_path
from ...utils import get_package_json_path
from ...utils import get_tailwind_src_path
from ...utils import install_pip_package
from ...validate import ValidationError
from ...validate import Validations


class Command(BaseCommand):
    help = "Runs tailwind commands"
    npm = None
    validate = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_standalone = None
        self.cwd = None
        self.validate = Validations()

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title="subcommands",
            description="Available tailwind subcommands",
            required=True,
            dest="subcommand",
        )

        # init subcommand
        init_parser = subparsers.add_parser(
            "init",
            help="Initialize django-tailwind app",
        )
        init_parser.add_argument(
            "--no-input",
            action="store_true",
            help="Initializes Tailwind project without user prompts",
        )
        init_parser.add_argument(
            "--tailwind-version",
            choices=["3", "4", "4s"],
            help="Specifies the Tailwind version to install",
        )
        init_parser.add_argument(
            "--app-name",
            help="Sets default app name on Tailwind project initialization",
        )
        init_parser.add_argument(
            "--include-daisy-ui",
            action="store_true",
            help="Includes DaisyUI component library in the Tailwind project",
        )
        init_parser.set_defaults(method=self.handle_init_command)

        # install subcommand
        install_parser = subparsers.add_parser(
            "install",
            help="Install npm packages necessary to build tailwind css",
        )
        install_parser.add_argument(
            "--no-package-lock",
            action="store_true",
            help="Disables package-lock.json creation during install",
        )
        install_parser.set_defaults(method=self.handle_install_command)

        # build subcommand
        build_parser = subparsers.add_parser(
            "build",
            help="Compile tailwind css into production css",
        )
        build_parser.set_defaults(method=self.handle_build_command)

        # start subcommand
        start_parser = subparsers.add_parser(
            "start",
            help="Start watching css changes for dev",
        )
        start_parser.set_defaults(method=self.handle_start_command)

        # dev subcommand
        dev_parser = subparsers.add_parser(
            "dev",
            help="Start Django server and Tailwind watcher simultaneously",
        )
        dev_parser.set_defaults(method=self.handle_dev_command)

        # check-updates subcommand
        check_updates_parser = subparsers.add_parser(
            "check-updates",
            help="List possible updates for tailwind css and its dependencies",
        )
        check_updates_parser.set_defaults(method=self.handle_check_updates_command)

        # update subcommand
        update_parser = subparsers.add_parser(
            "update",
            help="Update tailwind css and its dependencies",
        )
        update_parser.set_defaults(method=self.handle_update_command)

        # plugin_install subcommand
        plugin_install_parser = subparsers.add_parser(
            "plugin_install",
            help="Install and configure a tailwind plugin",
        )
        plugin_install_parser.add_argument(
            "plugin_name",
            help="Name of the plugin to install",
        )
        plugin_install_parser.set_defaults(method=self.handle_plugin_install_command)

    def validate_app(self):
        try:
            self.validate.has_settings()
            app_name = get_config("TAILWIND_APP_NAME")
            self.validate.is_installed(app_name)
            self.validate.is_tailwind_app(app_name)
        except ValidationError as err:
            return self.print_error(err)

    def handle(self, *args, method, **options):
        # Validate app for all commands except init
        if method != self.handle_init_command:
            self.validate_app()
            app_name = get_config("TAILWIND_APP_NAME")
            self.cwd = get_tailwind_src_path(app_name)
            self.npm = NPM(cwd=self.cwd)
            self.is_standalone = get_config("TAILWIND_USE_STANDALONE_BINARY") or not os.path.exists(
                get_package_json_path(app_name)
            )

        # Call the subcommand method
        method(**options)

    def handle_init_command(self, **options):
        app_name = options["app_name"].strip() if options.get("app_name") else None
        if not app_name:
            app_name_choice = input("Enter Tailwind app name [theme]: ")
            app_name = app_name_choice.strip() if app_name_choice.strip() else "theme"

        tailwind_version = (
            options["tailwind_version"].strip() if options.get("tailwind_version") else None
        )
        app_template_choice = {"4s": "1", "4": "2", "3": "3", None: None}[tailwind_version]
        if not app_template_choice:
            app_template_choice = input("""Choose template:
1 - Tailwind v4 Standalone - Simple and doesn't require Node.js
2 - Tailwind v4 Full - All the bells and whistles, requires Node.js
3 - Tailwind v3 Full - Legacy template for Tailwind v3 projects, requires Node.js
Enter choice [1-3]: """)
            self.validate_input(app_template_choice, ["1", "2", "3"])

        app_template = {
            "1": "app_template_v4_standalone",
            "2": "app_template_v4",
            "3": "app_template_v3",
        }[app_template_choice]

        include_daisy_ui = False
        if app_template != "app_template_v4_standalone":
            if options.get("no_input"):
                include_daisy_ui = options.get("include_daisy_ui", False)
            else:
                include_daisy_ui_choice = input("Include DaisyUI component library? (y/n): ")
                self.validate_input(include_daisy_ui_choice.lower(), ["y", "n"])
                include_daisy_ui = include_daisy_ui_choice.lower() == "y"

        self.install_app_template(
            app_template,
            app_name=app_name,
            include_daisy_ui=include_daisy_ui,
            no_input=True,
        )

    def handle_install_command(self, **options):
        if self.is_standalone:
            self.tailwind_cli_install_command()

            # Run the build command after installation
            self.tailwind_cli_build_command()
        else:
            args = ["install"]
            if options["no_package_lock"]:
                args.append("--no-package-lock")
            self.npm_command(*args)

            # Run the build command after installation
            self.npm_command("run", "build")

    def handle_build_command(self, **options):
        if self.is_standalone:
            self.tailwind_cli_build_command()
        else:
            self.npm_command("run", "build")

    def handle_start_command(self, **options):
        if self.is_standalone:
            self.tailwind_cli_start_command()
        else:
            self.npm_command("run", "start")

    def handle_dev_command(self, **options):
        if platform.system() == "Windows":
            return self.print_error(
                "The 'tailwind dev' command is not supported on Windows. "
                "Please run the Django development server and Tailwind watcher separately. "
                "Use 'python manage.py tailwind start' to start the Tailwind watcher."
            )

        self.maybe_install_honcho()
        procfile_path = self.get_or_create_procfile()
        self.print_dev_server_message(procfile_path)
        self.start_honcho()

    def handle_check_updates_command(self, **options):
        if self.is_standalone:
            return self.print_error(
                "Check-updates command is not supported for Tailwind projects that use standalone binary."
            )
        self.npm_command("outdated")

    def handle_update_command(self, **options):
        if self.is_standalone:
            return self.print_error(
                "Update command is not supported for Tailwind projects that use standalone binary."
            )
        self.npm_command("update")

    def handle_plugin_install_command(self, plugin_name, **options):
        if self.is_standalone:
            return self.print_error(
                "Plugin installation is not supported for Tailwind projects that use standalone binary."
            )

        # Install the npm package
        self.print(f"Installing {plugin_name} npm package...")
        try:
            self.npm_command("install", plugin_name, "--save-dev")
            self.print_success(f"Successfully installed {plugin_name} npm package")
        except Exception as err:
            return self.print_error(f"Failed to install {plugin_name}: {err}")

        # Update styles.css to include the plugin
        app_name = get_config("TAILWIND_APP_NAME")
        styles_path = os.path.join(get_tailwind_src_path(app_name), "src", "styles.css")

        if not os.path.exists(styles_path):
            return self.print_error(f"styles.css not found at {styles_path}")

        # Read current styles.css content
        with open(styles_path) as f:
            content = f.read()

        # Check if plugin is already included
        plugin_line = f'@plugin "{plugin_name}";'
        if plugin_line in content:
            return self.print_warning(f"Plugin {plugin_name} is already included in styles.css")

        # Add plugin line after @import "tailwindcss"
        import_line = '@import "tailwindcss";'
        if import_line not in content:
            return self.print_error('Could not find @import "tailwindcss"; in styles.css')

        # Insert plugin line after the import
        new_content = content.replace(import_line, f'{import_line}\n@plugin "{plugin_name}";\n')

        # Write updated content back to file
        with open(styles_path, "w") as f:
            f.write(new_content)

        self.print_success(f"Successfully added {plugin_name} to styles.css")
        self.print(f"Plugin {plugin_name} has been installed and configured!")

    def get_or_create_procfile(self):
        # Check if Procfile.tailwind exists, create if not
        procfile_path = os.path.join(os.getcwd(), "Procfile.tailwind")
        if not os.path.exists(procfile_path):
            self.stdout.write("Creating Procfile.tailwind...")
            procfile_content = """django: python manage.py runserver
tailwind: python manage.py tailwind start"""
            with open(procfile_path, "w") as f:
                f.write(procfile_content)
                self.print_success(
                    "Procfile.tailwind created! You can customize the Django runserver command in this file."
                )
        return procfile_path

    def install_app_template(self, app_template, app_name, include_daisy_ui, no_input):
        cookiecutter = self.get_or_install_cookiecutter()
        try:
            app_path = cookiecutter(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                output_dir=os.getcwd(),
                directory=app_template,
                no_input=no_input,
                overwrite_if_exists=False,
                extra_context={
                    "app_name": app_name,
                    "include_daisy_ui": "yes" if include_daisy_ui else "no",
                },
            )

            app_name = os.path.basename(app_path)

            self.print_success(
                f"Tailwind application '{app_name}' "
                f"has been successfully created. "
                f"Please add '{app_name}' to INSTALLED_APPS in settings.py, "
                f"and declare TAILWIND_APP_NAME = '{app_name}' in settings.py, "
                f"then run the following command to install Tailwind CSS "
                f"dependencies: `python manage.py tailwind install`"
            )

        except Exception as err:
            return self.print_error(err)

    def get_or_install_cookiecutter(self):
        try:
            from cookiecutter.main import cookiecutter
        except ImportError:
            self.print("Cookiecutter is not found, installing...")
            try:
                install_pip_package("cookiecutter")
                from cookiecutter.main import cookiecutter
            except ModuleNotFoundError:
                return self.print_error(
                    "Failed to install 'cookiecutter' via pip. Please install it manually "
                    "(https://pypi.org/project/cookiecutter/) and run 'python manage.py tailwind init' again."
                )
        return cookiecutter

    def maybe_install_honcho(self):
        # Check if honcho is installed
        try:
            subprocess.run(["honcho", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.install_honcho()

    def install_honcho(self):
        self.print("Honcho is not installed. Installing honcho...")
        try:
            install_pip_package("honcho")
            self.print_success("Honcho installed successfully!")
        except Exception:
            return self.print_error(
                "Failed to install 'honcho' via pip. Please install it manually "
                "(https://pypi.org/project/honcho/) and run 'python manage.py tailwind dev' again."
            )

    def start_honcho(self):
        # Start honcho with the Procfile
        try:
            subprocess.run(["honcho", "-f", "Procfile.tailwind", "start"], check=True)
        except subprocess.CalledProcessError as err:
            return self.print_error(f"Failed to start honcho: {err}")
        except KeyboardInterrupt:
            self.print("\nStopping development servers...")
            sys.exit(0)

    def print_dev_server_message(self, procfile_path):
        # Print a message with the server URL
        message = "🚀 Starting Tailwind watcher and Django development server"
        line = "#" * (len(message) + 1)

        self.print(line)
        self.print(message)
        if server_url := extract_server_url_from_procfile(procfile_path):
            self.print_success(f"   You can access the server at: {server_url}")
        self.print("   Press Ctrl+C to stop the servers")
        self.print(line)
        self.print("")

    def tailwind_cli_install_command(self):
        import pytailwindcss

        return pytailwindcss.install(
            version=get_config("TAILWIND_STANDALONE_BINARY_VERSION"),
        )

    def tailwind_cli_build_command(self):
        import pytailwindcss

        return pytailwindcss.run(
            shlex.split(get_config("TAILWIND_STANDALONE_BUILD_COMMAND_ARGS")),
            cwd=get_app_path(get_config("TAILWIND_APP_NAME")),
            live_output=True,
            auto_install=True,
            version=get_config("TAILWIND_STANDALONE_BINARY_VERSION"),
        )

    def tailwind_cli_start_command(self):
        try:
            import pytailwindcss

            pytailwindcss.run(
                shlex.split(get_config("TAILWIND_STANDALONE_START_COMMAND_ARGS")),
                cwd=get_app_path(get_config("TAILWIND_APP_NAME")),
                live_output=True,
                auto_install=True,
                version=get_config("TAILWIND_STANDALONE_BINARY_VERSION"),
            )
        except KeyboardInterrupt:
            sys.exit(0)

    def npm_command(self, *args):
        try:
            self.npm.command(*args)
        except NPMException as err:
            return self.print_error(err)
        except KeyboardInterrupt:
            sys.exit(0)

    def print(self, message):
        self.stdout.write(message)

    def print_success(self, message):
        self.print(self.style.SUCCESS(message))

    def print_warning(self, message):
        self.print(self.style.WARNING(message))

    def print_error(self, message):
        raise CommandError(message)

    def validate_input(self, user_input, valid_options):
        if user_input not in valid_options:
            return self.print_error(
                f"Invalid input '{user_input}'. Valid options are: {', '.join(valid_options)}"
            )
