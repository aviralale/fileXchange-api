import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import Folder
import shutil
import os

class Command(BaseCommand):
    help = 'Clean up old folders'

    def handle(self, *args, **options):
        # Specify the duration after which folders should be deleted (e.g., 7 days)
        duration = datetime.timedelta(days=7)

        # Calculate the threshold datetime for deletion
        threshold_datetime = timezone.now() - duration

        # Query for folders older than the threshold datetime
        folders_to_delete = Folder.objects.filter(created_at__lt=threshold_datetime)

        # Delete the folders and their contents
        for folder in folders_to_delete:
            folder_path = os.path.join('public/static/', str(folder.uid))
            shutil.rmtree(folder_path)
            folder.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up old folders.'))
