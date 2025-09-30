from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Initialize database with proper schema'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database...')
        
        # Run all migrations
        call_command('migrate', verbosity=0)
        
        # Check if the updated column exists
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(cart_order)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'updated' not in columns:
                self.stdout.write('Adding missing updated column...')
                cursor.execute("ALTER TABLE cart_order ADD COLUMN updated DATETIME DEFAULT CURRENT_TIMESTAMP")
                self.stdout.write(self.style.SUCCESS('Database initialized successfully'))
            else:
                self.stdout.write(self.style.SUCCESS('Database schema is up to date'))
