from django.db import models
import uuid
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Folder(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)

@receiver(post_delete, sender=Folder)
def delete_folder_files(sender, instance, **kwargs):
    # When a Folder instance is deleted, trigger the clean_folders management command
    os.system('python manage.py clean_folders')

def get_upload_path(instance, filename):
    return os.path.join(str(instance.folder.uid), filename)

class Files(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now=True)