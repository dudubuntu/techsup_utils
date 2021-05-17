from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class File(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)
    file = models.FileField()

    def __str__(self):
        return self.name

    def get_os_path(self):
        return settings.MEDIA_URL + self.name