import os

from cookiecutter.main import cookiecutter
from django.core.management.base import CommandError, LabelCommand

from tailwind import get_config

from ...npm import NPM, NPMException
from ...utils import get_tailwind_src_path
from ...validate import ValidationError, Validations


class Command(LabelCommand):
    help = "Runs tailwind commands"
    missing_args_message = """
Command argument is missing, please add one of the following:
  init - to initialize django-tailwind app
  install - to install npm packages necessary to build tailwind css
  build - to compile tailwind css into production css
  start - to start watching css changes for dev
  check-updates - to list possible updates for tailwind css and its dependencies
  update - to update tailwind css and its dependencies
Usage example:
  python manage.py tailwind start
"""
    npm = None
    validate = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.validate = Validations()

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--no-sync",
            action="store_true",
            help="Starts Tailwind dev server without browser sync",
        )
        parser.add_argument(
            "--no-jit",
            action="store_true",
            help="Initializes Tailwind project without JIT mode",
        )
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
            self.npm = NPM(cwd=get_tailwind_src_path(get_config("TAILWIND_APP_NAME")))

        getattr(self, "handle_" + labels[0].replace("-", "_") + "_command")(
            *labels[1:], **options
        )

    def handle_init_command(self, **options):
        try:
            app_path = cookiecutter(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                output_dir=os.getcwd(),
                directory="app_template_v2",
                no_input=options["no_input"],
                overwrite_if_exists=False,
                extra_context={
                    "app_name": options["app_name"]
                    if options.get("app_name")
                    else "theme",
                    "Tailwind build mode": "ahead of time (aot)"
                    if options.get("no_jit")
                    else "just in time (jit)",
                },
            )

            app_name = os.path.basename(app_path)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Tailwind application '{app_name}' "
                    f"has been successfully created. "
                    f"Please add '{app_name}' to INSTALLED_APPS in settings.py."
                )
            )
        except Exception as err:
            raise CommandError(err)

    def handle_install_command(self, **options):
        self.npm_command("install")

    def handle_build_command(self, **options):
        self.npm_command("run", "build")

    def handle_start_command(self, **options):
        if options.get("no_sync"):
            self.npm_command("run", "dev:postcss")
        else:
            self.npm_command("run", "start")

    def handle_check_updates_command(self, **options):
        self.npm_command("outdated")

    def handle_update_command(self, **options):
        self.npm_command("update")

    def npm_command(self, *args):
        try:
            self.npm.command(*args)
        except NPMException as err:
            raise CommandError(err)
        except KeyboardInterrupt:
            pass
