from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Prints static file configuration for debugging'

    def handle(self, *args, **options):
        self.stdout.write(f"BASE_DIR: {settings.BASE_DIR}")
        self.stdout.write(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")

        for static_dir in settings.STATICFILES_DIRS:
            exists = os.path.exists(static_dir)
            self.stdout.write(f"\nChecking: {static_dir}")
            self.stdout.write(f"Exists: {exists}")
            if exists:
                for root, dirs, files in os.walk(static_dir):
                    self.stdout.write(f"DIR: {root}")
                    for f in files:
                        full_path = os.path.join(root, f)
                        size = os.path.getsize(full_path)
                        readable = os.access(full_path, os.R_OK)
                        self.stdout.write(f"  FILE: {f} | size={size} bytes | readable={readable}")