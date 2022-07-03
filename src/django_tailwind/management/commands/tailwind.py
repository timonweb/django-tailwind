import os
from contextlib import contextmanager

import tailwind
from django.core.management.base import CommandError, LabelCommand

from django_tailwind import get_config

from ...utils import get_tailwind_src_path, install_pip_package
from ...validate import ValidationError, Validations


@contextmanager
def node_env(env: str):
    current = os.environ.get("NODE_ENV", "")
    os.environ["NODE_ENV"] = env
    yield
    os.environ["NODE_ENV"] = current


@contextmanager
def cd(path):
    current = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(current)


class Command(LabelCommand):
    help = "Runs tailwind commands"
    missing_args_message = """
Command argument is missing, please add one of the following:
  init - to initialize django-tailwind app
  build - to compile tailwind css into production css
  start - to start watching css changes for dev
Usage example:
  python manage.py tailwind start
"""
    cwd = None
    validate = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.validate = Validations()

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Initializes Tailwind project without user prompts",
        )
        parser.add_argument(
            "--app-name",
            help="Sets default app name on Tailwind project initialization",
        )

    def validate_app(self):
        try:
            self.validate.has_settings()
            app_name = get_config("TAILWIND_APP_NAME")
            self.validate.is_installed(app_name)
            self.validate.is_tailwind_app(app_name)
        except ValidationError as err:
            raise CommandError(err)

    def handle(self, *labels, **options):
        return self.handle_labels(*labels, **options)

    def handle_labels(self, *labels, **options):
        self.validate.acceptable_label(labels[0])
        if labels[0] != "init":
            self.validate_app()
            self.cwd = get_tailwind_src_path(get_config("TAILWIND_APP_NAME"))

        getattr(self, "handle_" + labels[0].replace("-", "_") + "_command")(*labels[1:], **options)

    def handle_init_command(self, **options):
        try:
            from cookiecutter.main import cookiecutter
        except ImportError:
            self.stdout.write("Cookiecutter is not found, installing...")
            install_pip_package("cookiecutter")
            from cookiecutter.main import cookiecutter

        try:
            app_path = cookiecutter(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                output_dir=os.getcwd(),
                directory="app_template",
                no_input=options["no_input"],
                overwrite_if_exists=False,
                extra_context={"app_name": options["app_name"].strip() if options.get("app_name") else "theme"},
            )

            app_name = os.path.basename(app_path)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Tailwind application '{app_name}' "
                    f"has been successfully created. "
                    f"Please add '{app_name}' to INSTALLED_APPS in settings.py, "
                    f"then run the following command to install Tailwind CSS "
                    f"dependencies: `python manage.py tailwind install`"
                )
            )
        except Exception as err:
            raise CommandError(err)

    def handle_build_command(self, **options):
        with node_env("production"), cd(self.cwd):
            tailwind.build(
                input="./src/styles.css",
                output="../static/css/dist/styles.css",
                minify=True,
                postcss=True,
            )

    def handle_start_command(self, **options):
        with node_env("development"), cd(self.cwd):
            tailwind.watch(
                input="./src/styles.css",
                output="../static/css/dist/styles.css",
                postcss=True,
            )
