from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update users without email addresses to have fallback emails'

    def handle(self, *args, **options):
        users_without_email = User.objects.filter(email='')
        updated_count = 0
        
        for user in users_without_email:
            user.email = f'user{user.id}@campus-shoppy.com'
            user.save()
            updated_count += 1
            self.stdout.write(f'Updated user {user.username} with email: {user.email}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} users with fallback emails')
        )
