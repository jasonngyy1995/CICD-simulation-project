import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('waiting for database...')
        db_connection = None
        while not db_connection:
            try:
                db_connection= connections['default']
            except OperationalError:
                self.stdout.write('database now unavailable, wait for a second')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('connect database successful!'))