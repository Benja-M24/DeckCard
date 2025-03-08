import sys
import time
import psycopg2
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Waits for database to be ready'

    def handle(self, *args, **options):
        max_retries = 10
        delay = 3  # seconds

        for retry in range(max_retries):
            try:
                connections['default'].ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database is ready!'))
                return
            except OperationalError:
                self.stdout.write(f'Database unavailable, waiting {delay} seconds (Attempt {retry + 1}/{max_retries})')
                time.sleep(delay)

        self.stderr.write(self.style.ERROR('Could not connect to the database after multiple attempts.'))
        sys.exit(1)
