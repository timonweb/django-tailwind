import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import LabelCommand, CommandError

from ...npm import NPM, NPMException
from ...utils import DJANGO_TAILWIND_APP_DIR, get_tailwind_src_path
from ...validate import ValidationError, Validations


class Command(LabelCommand):
    help = "Runs tailwind commands"
    missing_args_message = """
Command argument is missing, please add one of the following:
  init - to initialize django-tailwind app
  install - to install npm packages necessary to build tailwind css
  build - to compile tailwind css into production css
  start - to start watching css changes for dev
Usage example: 
  python manage.py tailwind start
"""
    npm = None
    validate = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.validate = Validations()

    def validate_app(self):
        try:
            self.validate.has_settings()
            app_name = getattr(settings, "TAILWIND_APP_NAME")
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
            self.npm = NPM(cwd=get_tailwind_src_path(settings.TAILWIND_APP_NAME))
        getattr(self, "handle_" + labels[0] + "_command")(*labels[1:], **options)

    def handle_init_command(self, app_name, **options):
        try:
            call_command(
                "startapp",
                app_name,
                template=os.path.join(DJANGO_TAILWIND_APP_DIR, "app_template"),
            )
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
        self.npm_command("run", "start")

    def npm_command(self, *args):
        try:
            self.npm.command(*args)
        except NPMException as err:
            raise CommandError(err)
        except KeyboardInterrupt:
            pass
