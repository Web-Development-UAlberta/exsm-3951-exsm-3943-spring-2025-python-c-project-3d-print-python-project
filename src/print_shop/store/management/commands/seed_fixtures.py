import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

FIXTURE_FILENAME = "seed_fixtures.json"
FIXTURE_PATH = os.path.join(settings.BASE_DIR, "store", "fixtures", FIXTURE_FILENAME)

class Command(BaseCommand):
    help = "Load pre-downloaded fixtures for models and images."

    def handle(self, *args, **options):
        if not os.path.exists(FIXTURE_PATH):
            self.stdout.write(self.style.ERROR(f"Fixture file not found: {FIXTURE_PATH}"))
            return

        try:
            self.stdout.write(self.style.SUCCESS(f"Loading fixture: {FIXTURE_PATH}"))
            call_command("loaddata", FIXTURE_PATH)
            self.stdout.write(self.style.SUCCESS("Fixture loaded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading fixture: {e}"))
