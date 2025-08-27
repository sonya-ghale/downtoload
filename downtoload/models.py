from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    downloaded_file = models.FileField(upload_to="videos/", blank=True, null=True)

    def __str__(self):
     return self.title