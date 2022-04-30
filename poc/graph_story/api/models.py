from django.db import models
from django.conf import settings

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)


class Graph(models.Model):
    name = models.CharField(max_length=255)
    folder = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, null=False)
    
    class Meta:
        unique_together = ('name', 'token',)
