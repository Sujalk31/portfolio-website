from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
import os


class Command(BaseCommand):
    help = 'Prints static file configuration for debugging'

    def handle(self, *args, **options):
        self.stdout.write(f"BASE_DIR: {settings.BASE_DIR}")
        self.stdout.write(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"STATICFILES_FINDERS: {settings.STATICFILES_FINDERS}")

        self.stdout.write("\n--- Using Django's actual finder logic ---")
        found_any = False
        for finder in get_finders():
            self.stdout.write(f"\nFinder: {finder.__class__.__name__}")
            for path, storage in finder.list([]):
                found_any = True
                self.stdout.write(f"  Found: {path} (storage root: {storage.location})")

        if not found_any:
            self.stdout.write("\n!!! NO FILES FOUND BY ANY FINDER !!!")