from django.core.management.base import AppCommand, BaseCommand, CommandError
from choices import create_models


class Command(BaseCommand):
    help = 'Runs file to create instances to fill development database'
    args = []
    # args = "[appname ...]"
    can_import_settings = True

    def handle(self, *args, **options):
        create_models