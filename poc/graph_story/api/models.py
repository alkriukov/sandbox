from django.db import models
from django.conf import settings

# Create your models here.
class Graph(models.Model):
    name = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

