import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

FIXTURE_FILENAME = "order_seed.json"


class Command(BaseCommand):
    help = "Load fixtures for orders, order items, and fulfillment status."

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.SUCCESS(f"Loading fixture: {FIXTURE_FILENAME}")
            )
            call_command("loaddata", FIXTURE_FILENAME)
            self.stdout.write(self.style.SUCCESS("Order fixtures loaded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading fixture: {e}"))
