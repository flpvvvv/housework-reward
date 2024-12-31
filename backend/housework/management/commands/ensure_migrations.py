from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ensures all migrations are run'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        call_command('migrate', verbosity=1, interactive=False)
        self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
