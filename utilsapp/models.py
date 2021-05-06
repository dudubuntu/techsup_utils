from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)
    file = models.FileField()

    def __str__(self):
        return self.name