from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if one does not already exist'

    def handle(self, *args, **options):
        username = config('ADMIN_USERNAME', default=None)
        password = config('ADMIN_PASSWORD', default=None)
        email = config('ADMIN_EMAIL', default='')

        if not username or not password:
            self.stdout.write(self.style.WARNING('ADMIN_USERNAME or ADMIN_PASSWORD not set — skipping.'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists — skipping.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))